import heapq
def small_nnum(list1,n):
  smallest=heapq.nsmallest(n,list1)
  return smallest