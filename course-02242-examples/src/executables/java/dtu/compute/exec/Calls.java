package dtu.compute.exec;

class Calls {

    @Case
    public static void helloWorld() {
        System.out.println("Hello, World!\n");
    }

    @Case
    public static int fib(int n) {
        if (n < 2) {
            return 1;
        } else {
            return fib(n - 1) + fib(n - 2);
        }
    }
}
