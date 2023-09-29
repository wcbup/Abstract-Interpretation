package eu.bogoe.dtu.exceptional;

import dtu.compute.exec.Case;

public class Arithmetics {

	@Case
	public static int alwaysThrows1() {
		return 4 / 0;
	}

	@Case
	public static int alwaysThrows2(int i) {
		int k = 3;
		k -= k;
		return i / k;
	}

	@Case
	public static float alwaysThrows3(float i, float j) {
		return i / j;
	}

	@Case
	public static int alwaysThrows4(int i, int j) {
		assert -1 <= j && j <= 1;
		return i / j;
	}

	@Case
	public static int alwaysThrows5(int i, int j) {
		if (i > 0) {
			j = 12;
		} else {
			i = -i;
		}
		return j / i;
	}

	@Case
	public static int itDependsOnLattice1() {
		int i = 3;
		i--;
		return 2 / i;
	}

	@Case
	public static int itDependsOnLattice2() {
		int i = -1000;
		i += 2;
		return 998 / i;
	}

	@Case
	public static int itDependsOnLattice3(int i, int j) {
		assert i > 1000;
		assert j > 10;
		for (int k = 0; k < 10; k++) {
			i -= j;
		}
		return j / i;
	}

	@Case
	public static int itDependsOnLattice4() {
		int i = 0;
		i++;
		i--;
		return 998 / i;
	}

	@Case
	public static int neverThrows1() {
		int i = 3;
		return 0 / i;
	}

	@Case
	public static int neverThrows2(int i) {
		assert i > 0;
		return 0 / i;
	}

	@Case
	public static int neverThrows3(int i, int j) {
		assert i > 0 && j == 0;
		j += i;
		j += i;
		j += i;
		return 0 / i;
	}

	@Case
	public static int neverThrows4(int i) {
		assert i > 0 && i < 0;
		return 0 / i;
	}

	@Case
	public static int neverThrows5(int i, int j) {
		if (i >= 0) {
			i++;
		} else {
			i = -i;
		}
		return j / i;
	}

	@Case
	public static int speedVsPrecision() {
		int i = 100000;
		while (i > 0) {
			i--;
		}
		return i / i;
	}
}
