package eu.bogoe.dtu.exceptional;

import dtu.compute.exec.Case;

public class Null {

	public Null field;

	@Case
	public static String alwaysThrows1() {
		Object obj = null;
		return obj.toString();
	}

	@Case
	public static void alwaysThrows2(Object o) {
		Null nil = new Null();
		if (nil.field.equals(nil)) {
			System.out.println("Equal");
		} else {
			System.out.println("Not Equal");
		}
	}

	@Case
	public static void alwaysThrows3(Object o) {
		Null nil = new Null();
		nil.field = new Null();
		if (nil.hashCode() == nil.field.hashCode()) {
			System.out.println("Equal");
		} else {
			System.out.println(nil.field.field.toString());
		}
	}

	@Case
	public static Object neverThrows1() {
		String obj = null;
		System.out.println(obj);
		return obj;
	}

	@Case
	public static void neverThrows2(Object o) {
		Null nil = new Null();
		if (nil.equals(nil.field)) {
			System.out.println("Equal");
		} else {
			System.out.println("Not Equal");
		}
	}

	@Case
	public static int neverThrows3(Integer i, Integer j) {
		assert i != null && j != null;
		if (i > j) {
			return i;
		}
		return j;
	}

	@Case
	public static boolean neverThrows4(Null n) {
		assert n == null;
		n = new Null();
		assert n != null;
		n.field = n;
		while (n != n.field) {
			n = null;
		}
		return n.equals(n.field);
	}

	@Case
	public static String neverThrows5(String s, String notYourProblem) {
		assert s != null;
		return s.concat(notYourProblem);
	}

	@Case
	public static Null interestingCase(Object o) {
		Null nil = new Null();
		nil.field = new Null();
		nil.field.field = new Null();
		while (!nil.field.equals(nil)) {
			nil = nil.field;
		}
		return nil;
	}
}
