package eu.bogoe.dtu.exceptional;

import dtu.compute.exec.Case;

public class Arrays {

	@Case
	public static void alwaysThrows1() {
		int[] is = new int[2];
		is[0] = 12;
		is[1] = 12;
		is[2] = 12;
	}

	@Case
	public static int alwaysThrows2(int[] is) {
		return is[0];
	}

	@Case
	public static void alwaysThrows3() {
		int[] spotTheError = new int[10];
		for (int i = 0; i <= spotTheError.length; i++) {
			spotTheError[i] = i;
		}
	}

	@Case
	public static void alwaysThrows4(float[] fs) {
		System.out.println(fs[fs.length - 1]);
	}

	@Case
	public static void alwaysThrows5(int i, int j) {
		assert i > 0 && j > 0;
		assert i < 10 && j < 10;
		int[] is = new int[1000];
		System.out.println(is[j - i]);
	}

	@Case
	public static int dependsOnLattice1(int[] is, int i) {
		assert 0 <= i && i < is.length;
		return is[i];
	}

	@Case
	public static int dependsOnLattice2(int[] is) {
		assert is.length > 0;
		int i = 2;
		i -= 2;
		return is[i];
	}

	@Case
	public static void dependsOnLattice3(float[] fs) {
		assert fs.length > 0;
		System.out.println(fs[fs.length - 1]);
	}

	@Case
	public static int dependsOnLattice4(int[] is) {
		assert is.length > 4;
		return is[0] + is[1] + is[2] + is[3] + is[4];
	}

	@Case
	public static int dependsOnLattice5(int i) {
		assert -10 < i && i < 10;
		int[] is = new int[10];
		if (i <= 0) {
			i = -i;
		} else {
			i--;
		}
		return is[i];
	}

	@Case
	public static int neverThrows1() {
		int[] is = new int[2];
		return is[0];
	}

	@Case
	public static int neverThrows2() {
		int[] is = new int[]{1, 2};
		return is[1];
	}

	@Case
	public static int neverThrows3() {
		int[] is = new int[5];
		int i = 0;
		for (int j = 0; j < 1000; j++) {
			i = is[i];
		}
		return i;
	}
}
