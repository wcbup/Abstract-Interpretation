package eu.bogoe.dtu;

import dtu.compute.exec.Case;

public class Integers {

    /**
     * Instructions:
     * - iconst_<i>
     * - istore_<n>
     * - return
     */
    @Case
    public static void smallConstant() {
        int a = 2;
    }

    /**
     * Instructions:
     * - istore_<n>
     * - return
     * - sipush
     */
    @Case
    public static void largeConstant() {
        int a = 1000;
    }

    /**
     * Instructions:
     * - istore_<n>
     * - ldc
     * - return
     */
    @Case
    public static void hugeConstant() {
        int a = 2147483647;
    }

    /**
     * Instructions:
     * - bipush
     * - iconst_<i>
     * - istore
     * - istore_<n>
     * - return
     */
    @Case
    public static void manyConstants() {
        int a = 1;
        int b = 2;
        int c = 3;
        int d = 4;
        int e = 5;
        int f = 6;
        int g = 7;
        int h = 8;
        int i = 9;
    }

    /**
     * Instructions:
     * - iand
     * - iconst_<i>
     * - iload
     * - iload_<n>
     * - ior
     * - ireturn
     * - ishl
     * - ishr
     * - istore
     * - istore_<n>
     * - iushr
     * - ixor
     */
    @Case
    public static int bitwiseLogic(int a, int b) {
        int and = a & b;
        int or = a | b;
        int xor = a ^ b;
        int shl = a << 2;
        int shr = b >> 2;
        int ushr = shl >>> 4;
        int neg = ~ushr;
        return neg;
    }

    /**
     * Instructions:
     * - iadd
     * - idiv
     * - iload
     * - iload_<n>
     * - imul
     * - ineg
     * - irem
     * - ireturn
     * - istore
     * - istore_<n>
     * - isub
     */
    @Case
    public static int arithmetic(int a, int b) {
        int add = a + a;
        int sub = b - a;
        int mul = add * sub;
        int div = a / b;
        int rem = mul % div;
        int neg = -rem;
        return neg;
    }

    /**
     * Instructions:
     * - aload_<n>
     * - areturn
     * - astore_<n>
     * - dup
     * - iaload
     * - iastore
     * - iconst_<i>
     * - newarray
     */
    @Case
    public static int[] intArray(int[] a) {
        int[] b = new int[]{a[0], a[1]};
        int[] c = new int[2];
        c[0] = b[1];
        c[1] = b[0];
        return c;
    }
}
