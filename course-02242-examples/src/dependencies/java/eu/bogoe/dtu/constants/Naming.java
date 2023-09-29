// Known Dependencies
// -> eu.bogoe.dtu.constants.Naming (eu/bogoe/dtu/constants/Naming.java)
// -> java.lang.String

package eu.bogoe.dtu.constants;

public class Naming {

    public static final int CONSTANT = 1;
    private String field = "name";

    protected static void methodName(Naming parameterName) {
        int variableName = 2;
        if (variableName > Naming.CONSTANT) {
            return;
        }
    }
}
