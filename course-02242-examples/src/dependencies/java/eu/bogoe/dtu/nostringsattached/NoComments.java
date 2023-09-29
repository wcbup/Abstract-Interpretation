// Known Dependencies
// -> eu.bogoe.dtu.nostringsattached.Ref1 (eu/bogoe/dtu/nostringsattached/Ref1.java)
// -> eu.bogoe.dtu.nostringsattached.Ref3 (eu/bogoe/dtu/nostringsattached/Ref3.java)
// -> eu.bogoe.dtu.nostringsattached.Ref4 (eu/bogoe/dtu/nostringsattached/Ref4.java)
// -> java.lang.String
// -> java.util.ArrayList

package eu.bogoe.dtu.nostringsattached;

import  java . util . ArrayList ; // "That white space..."

/**
 * Documentation is very important:
 * import eu.bogoe.dtu.nostringsattached.Ref2;
 */
class NoComments {

    public static void main(String[] args) {
        // /**
        Ref1 shouldBeThere = new Ref1();
        // **/
    }

    void regexChallanges() {
        String stringWithComment1 = "code // Comment"; Ref3 r3 = new Ref3();
        String stringWithComment2 = "code /* Comment */ code";
        String stringWithComment3 = "code /* Comment"; eu.bogoe.dtu.nostringsattached.Ref4 r4 = new eu.bogoe.dtu.nostringsattached.Ref4(); String stringWithComment4 = "Comment */ code";
        String escaping = " \" new Ref2() \" ";
        String importingString = " import eu.bogoe.dtu.nostringsattached.Ref2; ";
        /*
        Ref1 shouldNotThere = new Ref2();
        // * /
        "import eu.bogoe.dtu.nostringsattached.Ref2;"
        "new Ref2();"
        Ref2
        */
    }
}
