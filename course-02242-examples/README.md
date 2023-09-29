# Course 02242 - Examples

This repository contains a lot of different examples that can be analysed. 

## Building

To build the repository you should be able to simply run:

```
mvn package
```

Then the class files will be in the `target` folder.

## Dependencies `src/dependencies`

This subfolder contains examples of weird and non-weird dependencies and connections between class files.

In the top of all files there is an annotation which starts 
with `->`, which indicates the known dependencies of the files.

```
// -> dtu.compute.Example
// -> dtu.compute.Other
```

Means that the file depends on Example and Other.

Pull requests are welcome to add more interesting corner cases. 

## Executables `src/executables`

This subfolder contains examples of different executable programs, which we can use for analysis.

Every method annotated with `@Case` annotation should be considered a case.

