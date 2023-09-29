// Known Dependencies
// -> java.lang.Object
// -> java.lang.String
// -> java.lang.System

package eu.bogoe.dtu.autoimport;

import java.lang.String;
import java.lang.Object;

public class Manual extends Object {

    public static String method(Object o) {
        System.out.println(o);
        return "" + o;
    }
}
