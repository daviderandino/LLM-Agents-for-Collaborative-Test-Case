import pytest
from data.input_code.wb2 import *
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

@pytest.fixture
def upload_service():
    service = UploadService()
    yield service
    # Cleanup after each test
    for upload_id in list(service.uploads.keys()):
        service.delete_upload(upload_id)

@pytest.mark.parametrize('file_name, length, deferred_length, expected_deferred_length', [
    ("test.txt", 100, False, False),
    ("test.txt", None, True, True)
])
def test_create_upload(upload_service, file_name, length, deferred_length, expected_deferred_length):
    result = upload_service.create_upload(file_name, length, deferred_length)
    assert isinstance(result, UploadMetadata)
    assert result.file_name == file_name
    assert result.length == length
    assert result.deferred_length == expected_deferred_length

def test_get_upload(upload_service):
    upload_id = upload_service.create_upload("test.txt", 100, False).id
    result = upload_service.get_upload(upload_id)
    assert isinstance(result, UploadMetadata)
    assert result.id == upload_id

def test_get_upload_not_found(upload_service):
    with pytest.raises(UploadNotFound):
        upload_service.get_upload("non-existent")

def test_get_upload_gone(upload_service):
    upload_id = upload_service.create_upload("test.txt", 100, False).id
    meta = upload_service.uploads[upload_id]
    meta.is_terminated = True
    meta.offset = meta.length
    with pytest.raises(UploadGone):
        upload_service.get_upload(upload_id)

@pytest.mark.parametrize('length', [100])
def test_set_deferred_length(upload_service, length):
    upload_id = upload_service.create_upload("test.txt", None, True).id
    upload_service.set_deferred_length(upload_id, length)
    assert upload_service.uploads[upload_id].length == length
    assert upload_service.uploads[upload_id].deferred_length == False

def test_set_deferred_length_not_found(upload_service):
    with pytest.raises(UploadNotFound):
        upload_service.set_deferred_length("non-existent", 100)

@pytest.mark.parametrize('expected_offset, data', [(0, b"test")])
def test_append_chunk(upload_service, expected_offset, data):
    upload_id = upload_service.create_upload("test.txt", 100, False).id
    result = upload_service.append_chunk(upload_id, expected_offset, data)
    assert result == len(data)

def test_append_chunk_not_found(upload_service):
    with pytest.raises(UploadNotFound):
        upload_service.append_chunk("non-existent", 0, b"test")

def test_append_chunk_offset_mismatch(upload_service):
    upload_id = upload_service.create_upload("test.txt", 100, False).id
    with pytest.raises(OffsetMismatch):
        upload_service.append_chunk(upload_id, 10, b"test")

def test_delete_upload(upload_service):
    upload_id = upload_service.create_upload("test.txt", 100, False).id
    upload_service.delete_upload(upload_id)
    assert upload_id not in upload_service.uploads

def test_delete_upload_not_found(upload_service):
    with pytest.raises(UploadNotFound):
        upload_service.delete_upload("non-existent")

def test_cleanup_stale_uploads(upload_service):
    upload_id = upload_service.create_upload("test.txt", 100, False).id
    upload_service.uploads[upload_id].expires_at = datetime.now(timezone.utc)
    upload_service.cleanup_stale_uploads()
    assert upload_id not in upload_service.uploads

def test_list_uploads(upload_service):
    upload_service.create_upload("test.txt", 100, False)
    result = upload_service.list_uploads()
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.parametrize('file_name, length, deferred_length, expected_is_terminated', [
    ("test.txt", 0, False, True),
])
def test_create_upload_zero_length(upload_service, file_name, length, deferred_length, expected_is_terminated):
    result = upload_service.create_upload(file_name, length, deferred_length)
    assert result.is_terminated == expected_is_terminated

def test_set_deferred_length_smaller_than_offset(upload_service):
    upload_id = upload_service.create_upload("test.txt", None, True).id
    upload_service.uploads[upload_id].offset = 100
    with pytest.raises(UploadSizeException):
        upload_service.set_deferred_length(upload_id, 50)

def test_append_chunk_exceeds_declared_length(upload_service):
    upload_id = upload_service.create_upload("test.txt", 100, False).id
    with pytest.raises(UploadSizeException):
        upload_service.append_chunk(upload_id, 0, b"a" * 101)

def test_get_upload_forbidden(upload_service, monkeypatch):
    def mock_is_accessible_by_current_principal(meta):
        return False
    monkeypatch.setattr(upload_service, '_is_accessible_by_current_principal', mock_is_accessible_by_current_principal)
    upload_id = upload_service.create_upload("test.txt", 100, False).id
    with pytest.raises(ForbiddenException):
        upload_service.get_upload(upload_id)

def test_list_uploads_empty(upload_service):
    result = upload_service.list_uploads()
    assert isinstance(result, list)
    assert len(result) == 0

    from unittest.mock import patch, MagicMock

# --- COVERS LINE 43 (Lazy Lock Init) ---
def test_lock_lazy_initialization(upload_service):
    # 1. Create upload (creates lock)
    meta = upload_service.create_upload("test.txt", 100, False)
    
    # 2. Manually delete the lock to simulate it missing (memory cleanup/bug)
    del upload_service.upload_locks[meta.id]
    
    # 3. Accessing the lock should trigger Line 43 to recreate it
    lock = upload_service._lock_for(meta.id)
    assert lock is not None
    assert meta.id in upload_service.upload_locks

# --- COVERS LINE 69 (File Collision) ---
def test_create_upload_handles_existing_file_collision(upload_service):
    # 1. Define a fixed UUID to simulate collision
    fixed_uuid = "00000000-0000-0000-0000-000000000000"
    file_path = upload_service._file_for(fixed_uuid)
    
    # 2. Manually create the file so it "exists" before the service creates it
    file_path.touch()
    assert file_path.exists()

    # 3. Mock uuid4 to return our fixed ID
    with patch('uuid.uuid4', return_value=fixed_uuid):
        # 4. Create upload. This should see the file exists and run .unlink() (Line 69)
        upload_service.create_upload("test.txt", 100, False)
    
    # Verify file was recreated (still exists)
    assert file_path.exists()

# --- COVERS LINE 86 (Race Condition in get_upload) ---
def test_get_upload_race_condition(upload_service):
    meta = upload_service.create_upload("test.txt", 100, False)
    
    # Save original method to call later
    original_lock_for = upload_service._lock_for
    
    # Define a side effect that deletes the upload when the lock is requested
    def side_effect_delete_on_lock(uid):
        if uid in upload_service.uploads:
            del upload_service.uploads[uid]
        return original_lock_for(uid)
        
    # Patch _lock_for. 
    # Flow: get_upload checks "if in uploads" (PASS) -> calls _lock_for (DELETES UPLOAD) -> enters lock -> checks "if not meta" (FAIL/Line 86)
    with patch.object(upload_service, '_lock_for', side_effect=side_effect_delete_on_lock):
        with pytest.raises(UploadNotFound):
            upload_service.get_upload(meta.id)

# --- COVERS LINE 117 (Set Deferred on Non-Deferred) ---
def test_set_deferred_length_on_non_deferred_upload(upload_service):
    # 1. Create a non-deferred upload (length=100, deferred_length=False)
    upload_id = upload_service.create_upload("test.txt", 100, False).id
    
    # 2. Try to set length. Should trigger "if not meta.deferred_length: return" (Line 117)
    upload_service.set_deferred_length(upload_id, 200)
    
    # 3. Verify length was NOT changed
    assert upload_service.uploads[upload_id].length == 100

# --- VERIFIES LINE 156 (File Deletion) ---
def test_delete_upload_verifies_file_unlink(upload_service):
    meta = upload_service.create_upload("test.txt", 100, False)
    file_path = upload_service._file_for(meta.id)
    
    # 1. Assert file actually exists (If this fails, Line 156 is missed because create_upload failed)
    assert file_path.exists(), "File should exist after creation"
    
    # 2. Delete upload. Since file exists, Line 156 (unlink) MUST run.
    upload_service.delete_upload(meta.id)
    
    assert not file_path.exists()