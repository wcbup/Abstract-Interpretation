// Known Dependencies
// -> eu.bogoe.dtu.autoimport.Manual (eu/bogoe/dtu/autoimport/Manual.java)
// -> eu.bogoe.dtu.fullref.BuiltIns (eu/bogoe/dtu/fullref/BuiltIns.java)
// -> java.lang.String

package eu.bogoe.dtu.fullref;

public class Custom {

    public void test(String[] args) {
        eu.bogoe.dtu.autoimport.Manual.method(args);
        eu.bogoe.dtu.fullref.BuiltIns.main(args);
    }
}
