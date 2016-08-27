# coding=utf-8
s = 'abcdefg'
i = 2
tar = 'cdefgab'

s1 = s[i:] + s[0:i]

print s1


'''
http://blog.csdn.net/v_JULY_v/article/details/6322882

思路五、三步翻转法

    对于这个问题，咱们换一个角度，可以这么做：

将一个字符串分成两部分，X和Y两个部分，在字符串上定义反转的操作X^T，即把X的所有字符反转（如，X="abc"，那么X^T="cba"），那么我们可以得到下面的结论：(X^TY^T)^T=YX。显然我们这就可以转化为字符串的反转的问题了。

不是么?ok,就拿abcdef 这个例子来说，若要让def翻转到abc的前头，那么只要按下述3个步骤操作即可：
1、首先分为俩部分，X:abc，Y:def；
2、X->X^T，abc->cba， Y->Y^T，def->fed。
3、(X^TY^T)^T=YX，cbafed->defabc，即整个翻转。


'''