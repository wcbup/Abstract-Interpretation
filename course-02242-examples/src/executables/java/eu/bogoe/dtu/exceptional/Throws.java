package eu.bogoe.dtu.exceptional;

import dtu.compute.exec.Case;

public class Throws {

	@Case
	public static int alwaysThrows1() {
		throw new UnsupportedOperationException("Straight forward");
	}

	@Case
	public static void alwaysThrows2(int i) {
		assert i > 0;
		if (i - 1 > 0) {
			System.out.println("Ok");
		} else {
			throw new UnsupportedOperationException("Error");
		}
	}

	@Case
	public static void alwaysThrows3(int i) {
		if (i == 0) {
			i = 3;
		} else if (i < 0) {
			i = -i;
		} else {
			i++;
		}
		if (i > 0) {
			throw new UnsupportedOperationException("Positive Test");
		}
	}

	@Case
	public static void dependsOnLattice1(int i, int j) {
		if (i > j) {
			return;
		}
		if (i > j) {
			throw new UnsupportedOperationException("Straight forward");
		}
	}

	@Case
	public static void dependsOnLattice2() {
		int i = 0;
		i++;
		i--;
		if (i != 0) {
			throw new UnsupportedOperationException("How?");
		}
	}

	@Case
	public static void dependsOnLattice3(int i, int j) {
		while (i >= 0) {
			i /= 2;
			i--;
		}
		while (j < 0) {
			j /= 2;
		}
		j *= i;
		if (j == 0) {
			throw new UnsupportedOperationException("...");
		}
	}

	@Case
	public static void neverThrows1(int i) {
		if (i != i) {
			throw new UnsupportedOperationException("false");
		}
		if (false) {
			throw new UnsupportedOperationException("false");
		}
	}

	@Case
	public static void neverThrows2(int i, int j) {
		while (i >= 0) {
			i /= 2;
			i--;
		}
		while (j <= 0) {
			j /= 2;
			j++;
		}
		if (i < 0 && j > 0) {
			return;
		}
		throw new UnsupportedOperationException("How?");
	}

	@Case
	public static void neverThrows3(int i) {
		if (i == 0) {
			i = 3;
		} else if (i < 0) {
			i = -i;
		} else {
			i++;
		}
		if (i <= 0) {
			throw new UnsupportedOperationException("Negative Test");
		}
	}
}
