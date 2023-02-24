/*
 * @lc app=leetcode.cn id=4 lang=golang
 *
 * [4] 寻找两个正序数组的中位数
 */

// @lc code=start
func findMedianSortedArrays(nums1 []int, nums2 []int) float64 {
	return getKNumber(nums1, nums2, (len(nums1)+len(nums2))/2)
}

func getKNumber(nums1 []int, nums2 []int, k int) float64 {
	if len(nums1) < len(nums2) {
		return getKNumber(nums2, nums1, k)
	}
	if len(nums1) == 0 {
		return float64(nums2[k-1])
	}
	if len(nums2) == 0 {
		return float64(nums2[k-1])
	}
	p1 := (k - 1) / 2
	p2 := (k - 1) / 2
	if len(nums1) < p1 {
		p1 = len(nums1) - 1
		p2 = k - p1 - 1
	}
	if len(nums2) < p2 {
		p2 = len(nums2) - 1
		p1 = k - p2 - 1
	}
	if nums1[p1] > nums2[p2] {
		return getKNumber(nums2[p2+1:], nums1, k-p2-1)
	} else {
		return getKNumber(nums1[p1+1:], nums2, k-p1-1)
	}
}

// @lc code=end

