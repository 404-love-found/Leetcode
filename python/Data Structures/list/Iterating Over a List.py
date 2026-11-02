nums =[0,1,2,3,4,5]


#用 enumerate 同时获取索引和元素（推荐！）
for i,nums in enumerate(nums):
    print(f"Index: {i}, Value: {nums}")

#推荐用 enumerate，因为大部分时候你既需要索引又需要元素值。
#直接写 for i, val in enumerate(nums) 就行，比 for i in range(len(nums)) 然后再 nums[i] 取值要简洁得多。