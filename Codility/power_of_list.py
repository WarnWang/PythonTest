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


class Solution(object):
    def zigzagLevelOrder(self, root):
        node_list = [root]
        current_level_node_num = 0
        current_level_max_num = 1
        zigzag = [[]]
        switch_order = True
        while node_list:
            if current_level_node_num == current_level_max_num:
                if current_level_max_num == 0:
                    break
                zigzag.append([])
                current_level_max_num *= 2
                current_level_node_num = 0
                switch_order = not switch_order;
            node = node_list.pop(0)

            if node is not None:
                zigzag[-1].append(node.val)
                current_level_node_num += 1
                if switch_order:
                    node_list.append(node.left)
                    node_list.append(node.right)
                else:
                    node_list.append(node.right)
                    node_list.append(node.left)

            else:
                current_level_max_num -= 1

        if not zigzag[-1]:
            zigzag.pop()
        return zigzag


if __name__ == "__main__":
    print find_power([1, 2, 3])
