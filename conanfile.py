from conans import ConanFile, CMake, tools
from conans.tools import download, unzip
import os,shutil
from distutils.dir_util import copy_tree


class FelixarmadilloConan(ConanFile):
    name = "armadillo"
    version = "9.300.2"
    license = "Apache License 2.0"
    url = "https://github.com/i6-xx/armadillo-code"
    description = "Armadillo C++ linear algebra (matrix) library"
    settings = "cppstd", "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    build_policy = "missing"
    generators = "cmake"

    def source(self):
       
        tar = "http://sourceforge.net/projects/arma/files/{}-{}.tar.xz".format(self.name,self.version)
        tools.get(tar)
        os.chdir('{}-{}'.format(self.name,self.version))
        copy_tree(".", "..")
        os.chdir('..')
        shutil.rmtree('{}-{}'.format(self.name,self.version))

        

    def build(self):
        tools.replace_in_file(file_path="include/armadillo_bits/config.hpp",
                              search="#define ARMA_USE_LAPACK",
                              replace="//#define ARMA_USE_LAPACK")

        tools.replace_in_file(file_path="include/armadillo_bits/config.hpp",
                              search="#define ARMA_USE_BLAS",
                              replace="//#define ARMA_USE_BLAS")
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("armadillo", dst="include", src="include")
        self.copy("*.hpp", dst="include/armadillo_bits", src="include/armadillo_bits")
        self.copy("*armadillo.dll", dst="bin", keep_path=False)
        self.copy("*armadillo.lib", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["armadillo"]
