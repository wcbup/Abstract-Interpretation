// Known Dependencies
// -> java.lang.ArithmeticException
// -> java.lang.ArrayStoreException
// -> java.lang.CloneNotSupportedException
// -> java.lang.Double
// -> java.lang.Float
// -> java.lang.Long
// -> java.lang.String

package eu.bogoe.dtu.autoimport;

public class Auto {

    static Long method(Double d) throws CloneNotSupportedException, ArrayStoreException {
        if (d > 0) {
            throw new ArithmeticException();
        }
        String s = "1.3";
        return (long)Float.parseFloat(s);
    }
}
