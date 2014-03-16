fuzzing
======

This package contains everything for fuzzing/testing inputs. 

## Fuzzing Setup

The main entry point is defined in test.py. We implemented a 'pseudo' Strategy Pattern for exploits. The exploit_strategy object contains all the assets as well as common methods used for multiple exploits. It is given a concrete strategy (i.e., sanitiazion_exploit) that overrides its execute method. The concrete_strategy is passed inside this method, allowing reuse of all functions and access to all assets. This allows for code reuse and allow each "strategy" to differ in their behavior. 
