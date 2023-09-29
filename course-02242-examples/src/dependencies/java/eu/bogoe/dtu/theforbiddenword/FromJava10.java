// Known Dependencies
// -> eu.bogoe.dtu.theforbiddenword.NormalClass (eu/bogoe/dtu/theforbiddenword/NormalClass.java)

package eu.bogoe.dtu.theforbiddenword;

public class FromJava10 {

    void doNotUseTheWord() {
        var guessTheType = NormalClass.create();
        guessTheType.sayHello();
    }
}
