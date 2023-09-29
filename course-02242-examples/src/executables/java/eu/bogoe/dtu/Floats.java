package eu.bogoe.dtu;

import dtu.compute.exec.Case;

public class Floats {

    /**
     * Instructions:
     * - fconst_<f>
     * - fstore_<n>
     * - return
     */
    @Case
    public static void smallConstant() {
        float a = 2.0f;
    }

    /**
     * Instructions:
     * - fstore_<n>
     * - ldc
     * - return
     */
    @Case
    public static void hugeConstant() {
        float a = 2023e35f;
    }

    /**
     * Instructions:
     * - fconst_<n>
     * - fstore
     * - fstore_<n>
     * - ldc
     * - return
     */
    @Case
    public static void manyConstants() {
        float a = 1;
        float b = 2;
        float c = 3;
        float d = 4;
        float e = 5;
        float f = 6;
        float g = 7;
        float h = 8;
        float i = 9;
    }

    /**
     * Instructions:
     * - fadd
     * - fdiv
     * - fload
     * - fload_<n>
     * - fmul
     * - fneg
     * - frem
     * - freturn
     * - fstore
     * - fstore_<n>
     * - fsub
     */
    @Case
    public static float arithmetic(float a, float b) {
        float add = a + a;
        float sub = b - a;
        float mul = add * sub;
        float div = a / b;
        float rem = mul % div;
        float neg = -rem;
        return neg;
    }

    /**
     * Instructions:
     * - aload_<n>
     * - areturn
     * - astore_<n>
     * - dup
     * - faload
     * - fastore
     * - iconst_<i>
     * - newarray
     */
    @Case
    public static float[] floatArray(float[] a) {
        float[] b = new float[]{a[0], a[1]};
        float[] c = new float[2];
        c[0] = b[1];
        c[1] = b[0];
        return c;
    }
}
