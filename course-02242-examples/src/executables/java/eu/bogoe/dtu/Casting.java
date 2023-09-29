package eu.bogoe.dtu;

import dtu.compute.exec.Case;

public class Casting {

    /**
     * Instructions:
     * - f2i
     * - fload_<n>
     * - fstore_<n>
     * - i2b
     * - i2c
     * - i2f
     * - i2s
     * - iload
     * - iload_<n>
     * - ireturn
     * - istore
     * - istore_<n>
     */
    @Case
    public static int simpleDataTypes(int in) {
        float f = (float)in;
        short s = (short)f;
        byte b = (byte)s;
        char c = (char)b;
        return (int)c;
    }

    /**
     * Instructions:
     * - aload_<n>
     * - areturn
     * - astore_<n>
     * - checkcast
     */
    @Case
    public static String reference(String in) {
        Object o = in;
        String s = (String)o;
        return s;
    }
}
