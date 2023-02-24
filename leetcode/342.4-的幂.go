/*
 * @lc app=leetcode.cn id=342 lang=golang
 *
 * [342] 4的幂
 */

// @lc code=start
func isPowerOfFour(n int) bool {
	return n > 0 && n & (n - 1) ==0 && n & 0xaaaaaaaa == 0
}
// @lc code=end

