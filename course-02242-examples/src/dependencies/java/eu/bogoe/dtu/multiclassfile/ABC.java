// Known Dependencies
// -> eu.bogoe.dtu.multiclassfile.D (eu/bogoe/dtu/multiclassfile/D.java)
// -> eu.bogoe.dtu.multiclassfile.J (eu/bogoe/dtu/multiclassfile/D.java)

package eu.bogoe.dtu.multiclassfile;

import eu.bogoe.dtu.multiclassfile.D;
import eu.bogoe.dtu.multiclassfile.J;

public class ABC {

    public static void abcd() {
        A a = new A();
        B b = new B();
        C c = new C();
        D d = new D();
    }
}

class A {

    private ABC i;

    public A() {
        i = new ABC();
    }
}

class B {
    public J j = new J();
}

class C {
    static final B q = new B();
}
