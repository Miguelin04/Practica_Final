class MergeSort:
    def __init__(self):
        self.buffer = None

    def sort_primitive_ascendent(self, nums):
        self.buffer = [0] * len(nums)
        self.merge_sort(nums, 0, len(nums) - 1)
        return nums

    def sort_primitive_descendent(self, nums):
        self.buffer = [0] * len(nums)
        self.merge_sort(nums, 0, len(nums) - 1)
        return nums[::-1]

    def sort_models_ascendent(self, array, attribute):
        self.buffer = [0] * len(array)
        self.merge_sort(array, 0, len(array) - 1, attribute)
        return array

    def sort_models_descendent(self, array, attribute):
        self.buffer = [0] * len(array)
        self.merge_sort(array, 0, len(array) - 1, attribute)
        return array[::-1]

    def merge_sort(self, nums, start, end, attribute=None):
        if start < end:
            mid = (start + end) // 2
            self.merge_sort(nums, start, mid, attribute)
            self.merge_sort(nums, mid + 1, end, attribute)
            self.merge_two_arrays(nums, start, mid, end, attribute)

    def merge_two_arrays(self, nums, start, mid, end, attribute=None):
        left = start
        right = mid + 1
        i = start

        while left <= mid and right <= end:
            if attribute:
                if getattr(nums[left], attribute) <= getattr(nums[right], attribute):
                    self.buffer[i] = nums[left]
                    left += 1
                else:
                    self.buffer[i] = nums[right]
                    right += 1
            else:
                if nums[left] <= nums[right]:
                    self.buffer[i] = nums[left]
                    left += 1
                else:
                    self.buffer[i] = nums[right]
                    right += 1
            i += 1

        while left <= mid:
            self.buffer[i] = nums[left]
            left += 1
            i += 1

        while right <= end:
            self.buffer[i] = nums[right]
            right += 1
            i += 1

        for j in range(start, end + 1):
            nums[j] = self.buffer[j]
