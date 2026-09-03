SHELL := /bin/bash
CXX ?= g++
CXXFLAGS := -std=c++20 -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror
BUILD := build

.PHONY: test test-python test-cpp test-lean hashes clean

test: test-python test-cpp

$(BUILD):
	mkdir -p $(BUILD)

test-python:
	cd tools/mirror-cut && python3 test_mirror_cut.py

test-cpp: $(BUILD)
	$(CXX) $(CXXFLAGS) tools/cpp/atomic_reference_kernel.cpp -o $(BUILD)/atomic_reference_kernel
	$(BUILD)/atomic_reference_kernel
	$(CXX) $(CXXFLAGS) tools/cpp/claim_motion_gate.cpp -o $(BUILD)/claim_motion_gate
	$(BUILD)/claim_motion_gate

test-lean:
	@command -v lean >/dev/null || { echo "Lean not found. Install the pinned toolchain from tools/moneyroot/lean-toolchain."; exit 2; }
	lean tools/moneyroot/MoneyRoot_v0_2.lean

hashes:
	./scripts/hash_repository.sh

clean:
	rm -rf $(BUILD)
