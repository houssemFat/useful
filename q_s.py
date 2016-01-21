"""
	Quick sort naive impelementation
	1- pick a pivot 
	2- partition 
		* choose an index (partition_index cursor index here)
		* if the current is less than the pivot then 
			swap this value with the value of c_index (latest modified index)
	
"""
def quick_sort(list):
  print "list >>> "
  if len(list) < 2 :
	return list
  print list
  pivot = list[len(list) -1]
  partition_index = 0
  swap_value = 0 
  print "pivot >>> %d " % pivot
  for (index, current) in enumerate(list):
	if (current < pivot) :
		# here a new element less than the pivot  
		swap_value = list[partition_index]
		list[index] = swap_value
		list[partition_index] = current
		print "swap %d with %d" % (swap_value, current)
		# increments current partition index 
		partition_index = partition_index + 1
  # return the 2 partition 
  return quick_sort(list[:partition_index]) + [pivot]  +  quick_sort (list[partition_index:len(list)-1])
		
if __name__ == "__main__" :
	print quick_sort([7, 2, 1, 6, 8, 5, 3, 0, 4])
