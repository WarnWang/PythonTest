def find_power(nums):
    if nums is None or len(nums) == 0:
        return [[]]

    n = len(nums)
    if n == 1:
        return [[], [nums[0]]]

    result = find_power(nums[1:])
    temp_result = []
    for i in result:
        j = i[:]
        j.append(nums[0])
        temp_result.append(j)

    result.extend(temp_result)
    return result


if __name__ == "__main__":
    print find_power([1, 2, 3])
