package eu.bogoe.dtu.exceptional;

import dtu.compute.exec.Case;

public class NullArrays {

	@Case
	public static void alwaysThrows1() {
		String[] ss = new String[2];
		System.out.println(ss[1].toString());
	}

	@Case
	public static String alwaysThrows2(Object[] os) {
		assert os.length > 0;
		return os[0].toString();
	}

	@Case
	public static void dependsOnAmalgamation1() {
		String[] ss = new String[2];
		ss[0] = "1";
		ss[1] = "2";
		System.out.println(ss[0].equals(ss[1]));
	}

	@Case
	public static void dependsOnAmalgamation2() {
		String[] ss = new String[10000];
		ss[0] = "1";
		ss[1] = "2";
		System.out.println(ss[0].equals(ss[1]));
	}
}
