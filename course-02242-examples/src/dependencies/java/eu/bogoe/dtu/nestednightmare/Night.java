// Known Dependencies
// -> java.lang.SecurityException
// -> java.lang.System

package eu.bogoe.dtu.nestednightmare;

public class Night {

    static public class Mare {
        void wakeUp() throws SecurityException {
            throw new java.lang.SecurityException("import eu.bogoe.dtu.nestednightmare.Night.Mare;");
        }
    }

    public class Meal {
        static void eat(int weight) {
            System.out.println("Eating " + weight + " grams of food.");
        }
    }
}
