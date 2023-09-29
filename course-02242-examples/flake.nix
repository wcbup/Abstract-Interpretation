{
  description = "Java examples";

  inputs =
    {
      nixpkgs.url = "github:NixOS/nixpkgs/23.05";
      flake-utils.url = "github:numtide/flake-utils";
    };
  outputs = { self, nixpkgs, flake-utils, ... }@inputs:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells = {
          default = pkgs.mkShell {
            name = "course-02242-examples";
            packages = (with pkgs; [ java-language-server jdk maven ]);
          };
        };
      });
}
