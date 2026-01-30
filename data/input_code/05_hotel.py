import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

# Custom Exceptions to test error handling
class RoomNotFoundError(Exception):
    """Raised when the requested room does not exist."""
    pass

class RoomUnavailableError(Exception):
    """Raised when the room is already occupied for the requested dates."""
    pass

class InvalidDateError(Exception):
    """Raised when dates are inconsistent (e.g., checkout before checkin)."""
    pass

class ReservationNotFoundError(Exception):
    """Raised when attempting to cancel a non-existent reservation."""
    pass

@dataclass
class Reservation:
    reservation_id: str
    room_number: int
    user_name: str
    check_in: datetime.date
    check_out: datetime.date
    total_price: float

class HotelReservationSystem:
    def __init__(self):
        # Format: {room_number: {'type': str, 'price_per_night': float}}
        self.rooms: Dict[int, Dict] = {}
        # Format: {reservation_id: Reservation object}
        self.reservations: Dict[str, Reservation] = {}
        self._reservation_counter = 0

    def add_room(self, room_number: int, room_type: str, price_per_night: float) -> None:
        """Adds a room to the system. Overwrites if it already exists."""
        if price_per_night <= 0:
            raise ValueError("Price per night must be positive.")
        
        self.rooms[room_number] = {
            'type': room_type,
            'price_per_night': price_per_night
        }

    def _is_room_available(self, room_number: int, check_in: datetime.date, check_out: datetime.date) -> bool:
        """Checks if a room is available in a given date range."""
        for res in self.reservations.values():
            if res.room_number == room_number:
                # Date overlap logic:
                # (StartA < EndB) and (EndA > StartB)
                if check_in < res.check_out and check_out > res.check_in:
                    return False
        return True

    def book_room(self, room_number: int, user_name: str, check_in: datetime.date, check_out: datetime.date) -> str:
        """
        Books a room. Returns the reservation ID.
        Raises exceptions if the room doesn't exist, dates are invalid, or the room is occupied.
        """
        if room_number not in self.rooms:
            raise RoomNotFoundError(f"Room {room_number} does not exist.")

        if check_in >= check_out:
            raise InvalidDateError("Check-out date must be after check-in date.")

        if check_in < datetime.date.today():
            raise InvalidDateError("Cannot book in the past.")

        if not self._is_room_available(room_number, check_in, check_out):
            raise RoomUnavailableError(f"Room {room_number} is not available for these dates.")

        # Calculate price
        nights = (check_out - check_in).days
        price_per_night = self.rooms[room_number]['price_per_night']
        total_price = round(nights * price_per_night, 2)

        # Create reservation
        self._reservation_counter += 1
        res_id = f"RES-{self._reservation_counter:04d}"
        
        new_reservation = Reservation(
            reservation_id=res_id,
            room_number=room_number,
            user_name=user_name,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price
        )
        
        self.reservations[res_id] = new_reservation
        return res_id

    def cancel_reservation(self, reservation_id: str) -> float:
        """
        Cancels a reservation and returns the refund amount.
        Refund Policy:
        - > 7 days from check-in: 100% refund
        - 2-7 days from check-in: 50% refund
        - < 2 days from check-in: 0% refund
        """
        if reservation_id not in self.reservations:
            raise ReservationNotFoundError("Reservation not found.")

        reservation = self.reservations.pop(reservation_id)
        days_until_checkin = (reservation.check_in - datetime.date.today()).days

        if days_until_checkin > 7:
            return reservation.total_price
        elif 2 <= days_until_checkin <= 7:
            return round(reservation.total_price * 0.5, 2)
        else:
            return 0.0

    def get_room_occupancy(self, date: datetime.date) -> List[int]:
        """Returns a list of occupied room numbers for a specific date."""
        occupied_rooms = []
        for res in self.reservations.values():
            # A room is occupied if the requested date is >= check_in and < check_out
            if res.check_in <= date < res.check_out:
                occupied_rooms.append(res.room_number)
        return sorted(occupied_rooms)