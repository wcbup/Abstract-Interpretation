package dtu.compute.exec;

class Array {

    @Case
    public static int first(int[] vals) {
        return vals[0];
    }

    @Case
    public static int firstSafe(int[] vals) {
        assert vals.length >= 1;
        return vals[0];
    }

    @Case
    public static int access(int i, int[] vals) {
        return vals[i];
    }

    @Case
    public static int newArray() {
        int vals[] = {1, 2, 3};
        return vals[0];
    }

    @Case
    public static int newArrayOutOfBounds() {
        int vals[] = {1, 2, 3};
        return vals[4];
    }

    @Case
    public static int accessSafe(int i, int[] vals) {
        assert 0 <= i;
        assert i < vals.length;
        return vals[i];
    }

    @Case
    public static void bubbleSort(int[] vals) {
        int n = vals.length;
        while (n > 1) {
            int next_n = 0;
            for (int i = 1; i < n ; i++) {
                if (vals[i - 1] > vals[i]) {
                    int tmp = vals[i - 1];
                    vals[i - 1] = vals[i];
                    vals[i] = tmp;
                    next_n = i;
                }
            }
            n = next_n;
        }
    }

    @Case
    public static int aWierdOneOutOfBounds() {
        int vals[] = {0,1,4};
        return vals[vals[2]];
    }

    @Case
    public static int aWierdOneWithinBounds() {
        int vals[] = {0,1,4};
        return vals[vals[1]];
    }
}
