// Known Dependencies
// -> java.lang.Integer
// -> java.lang.Long
// -> java.lang.String
// -> java.lang.System
// -> java.util.Arrays

package eu.bogoe.dtu.fullref;

public class BuiltIns {

    public static void main(java.lang.String[] args) {
        java.lang.Integer i = 3;
        java.lang.System.out.println(java.util.Arrays.toString(new int[]{i, java.lang.Long.BYTES}));
    }
}
