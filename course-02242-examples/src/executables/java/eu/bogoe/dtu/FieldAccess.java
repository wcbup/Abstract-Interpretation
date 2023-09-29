package eu.bogoe.dtu;

import dtu.compute.exec.Case;

public class FieldAccess {

    public static final int INT_CONSTANT = 3;
    public static final String STRING_CONSTANT = "Constant";
    public static float floatStatic = 1.0f;
    public static Object objectStatic = (Integer)2;

    public final byte BYTE_INSTANCE_CONSTANT;
    public final Object OBJECT_INSTANCE_CONSTANT;
    public float floatField;
    public String stringField = "Field";

    /**
     * Instructions:
     * - fconst_<f>
     * - iconst_<i>
     * - invokestatic
     * - putstatic
     * - return
     */
    static {}

    /**
     * Instructions:
     * - aload_<n>
     * - f2i
     * - fload_<n>
     * - i2b
     * - invokespecial
     * - invokestatic
     * - ldc
     * - putfield
     * - return
     */
    public FieldAccess(float f) {
        this.BYTE_INSTANCE_CONSTANT = (byte)f;
        this.OBJECT_INSTANCE_CONSTANT = (Float)f;
        this.floatField = f;
    }

    /**
     * Instructions:
     * - fadd
     * - getstatic
     * - ldc
     * - putstatic
     * - return
     */
    @Case
    public static void statics() {
        FieldAccess.floatStatic += FieldAccess.INT_CONSTANT;
        FieldAccess.objectStatic = FieldAccess.objectStatic;
        FieldAccess.objectStatic = FieldAccess.STRING_CONSTANT;
    }

    /**
     * Instructions:
     * - aload_<n>
     * - areturn
     * - astore_<n>
     * - dup
     * - fconst_<f>
     * - fmul
     * - getfield
     * - i2f
     * - invokespecial
     * - ldc
     * - new
     * - putfield
     */
    @Case
    public static Object instances() {
        FieldAccess fa1 = new FieldAccess(2.0f);
        FieldAccess fa2 = new FieldAccess(0.0f);
        fa2.floatField *= fa1.BYTE_INSTANCE_CONSTANT;
        fa1.stringField = "123";
        return fa2.OBJECT_INSTANCE_CONSTANT;
    }
}
