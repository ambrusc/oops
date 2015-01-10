# Ambrus Csaszar 1/9/2015

""" A real-world implementation of the 'Taboo' problem... """

import collections


def build_rules_from_iterable(iterable):
    rules = collections.defaultdict(set)
    last_item = None
    for item in iterable:
        if last_item is not None:
            rules[last_item].add(item)
        last_item = item
    return rules


def apply_rules(rules, iterable):
    """
    omits invalid elements from an iterable based on a set of rules

    @params
    rules : `dict` of (`item` => `set` of `item`)
        maps each key to a set of items that should not immediately follow that
        key in the input iterable
    iterable : `iterable`
        contains potentially invalid items

    @returns
    an iterable without invalid items
    """
    ret = []
    for item in iterable:
        if len(ret):
            last_item = ret[-1]
            exclusion_set = rules.get(last_item, None)
            if (exclusion_set is not None) and (item in exclusion_set):
                continue
        ret.append(item)
    return ret


def main():
    # Define an arbitrary set of rules in an arbitrary format
    rule_list = ["a", "c", "a", "b"]
    # Convert rules to our desired format
    rules = build_rules_from_iterable(rule_list)
    # Define an arbitrary test input
    test_list = ["a", "c", "b", "x", "c", "a"]
    # Apply our rules to the test input
    result_list = apply_rules(rules, test_list)
    # Show the results
    print result_list


if __name__ == "__main__":
    main()



# FAQ:
# 1. Why is there no `Taboo` class?
#       A: We don't need it (and it didn't have a very descriptive name).
#
# 2. What if we want to apply the same set of rules to multiple inputs?
#       A:
def _apply_rules_to_many_inputs():
    # Define an arbitrary set of rules in an arbitrary format
    rule_list = ["a", "c", "a", "b"]
    # Convert rules to our desired format
    rules = build_rules_from_iterable(rule_list)
    # Inputs (can be pulled from anywhere via any means)
    inputs = [
        ["a", "c", "b", "x", "c", "a"],
        ["a", "c", "b", "x", "c", "a"],
        ["a", "c", "b", "x", "c", "a"],
        ["a", "c", "b", "x", "c", "a"],
    ]
    # Apply rules to each input
    results = map(lambda i: apply_rules(rules, i), inputs)
    # Alternatively
    results = []
    for i in inputs:
        results.append(apply_rules(rules, i))

# 3. Haven't we made the code longer by not using a class for encapsulation?
#       A: Have we?
class Taboo(object):
    def __init__(self, rule_list):
        self.rules = build_rules_from_iterable(rule_list)

    def noFollow(self, item):
        return self.rules[item]

    def reduce(self, iterable):
        return apply_rules(self.rules, iterable)

def _apply_rules_to_many_inputs_with_class():
    # Define an arbitrary set of rules in an arbitrary format
    rule_list = ["a", "c", "a", "b"]
    # Convert rules to our desired format
    rule_applicator = Taboo(rule_list)
    # Inputs (can be pulled from anywhere via any means)
    inputs = [
        ["a", "c", "b", "x", "c", "a"],
        ["a", "c", "b", "x", "c", "a"],
        ["a", "c", "b", "x", "c", "a"],
        ["a", "c", "b", "x", "c", "a"],
    ]
    # Apply rules to each input
    results = map(lambda i: rule_applicator.reduce(i), inputs)
    # Alternatively
    results = []
    for i in inputs:
        results.append(rule_applicator.reduce(i))

# 4. Hey! Now you have to remember to pass a `rules` object to your `apply_rules`
#       function!
#       A: Yes, we're creating rules directly and passing it to a transformation
#           with two inputs. The OOP style method has the same characteristics
#           (two inputs, one output), execpt that it assumes certain inputs are
#           more important than other inputs:
#               functional style: "<output> = [transformation](<input>, <input>)"
#               OOP style: "<output> = <INPUT>.[transformation](<input>)"
#
# 5. But it's true! It's obvious that the rules can be reused so they're more
#       important!
#       A: Ultimately, we care about the output. We write code to take `stuff`
#           and turn it into `more useful stuff`. The more useful stuff is the output.
#           If either `the rules` or `the input list` is missing, we get no output and
#           our code is useless. In that sense, both inputs are equally important.
#
# 6. Can't we just choose the input that changes least frequently, wrap it in a
#       class and write methods on that class by convetion?
#       A: This isn't a useful distinction. For one, it's easy to find a
#           transformation that needs more than two inputs, where each input
#           changes with different, nonconstant frequency.
#
# 7. I can pick a better convention by which to designate the most important data
#       for each transformation.
#       A: We've already seen that we can't get output without all of the requisite
#           inputs so any distinction is arbitrary. Worse yet, different programmers
#           will choose different conventions. Nobody's objectively right, and we're
#           left with a codebase where transformations are arbitrarily tied to one of
#           their inputs or another.
#
# 8. The convention might be arbitrary, but I can just move methods to another
#       object if I need to refactor.
#       A: There are two use cases to consider:
#           1. code maintainers need a reasonable organization to navigate
#               implementation details
#           2. code users need a reasonably exposed API that's easy to understand
#               and relatively stable
#       (If both 1. and 2. are the same person, you're lucky - many times that's
#       not the case, but either way it doesn't matter... read on.)
#
#       Moving methods might seem simple but it has a hidden cost. At best,
#       you're required to change the argument list because the 'this' or 'self'
#       object has to come first (or is passed implicitly). Done? Not so fast.
#
#       By changing the argument list, you've just broken all code that ever
#       called your transformation.
#
#       Pause and think about that for a moment.
#
#       You've tried to satisfy use case 1. and you've created a mess of use case 2.
#
#       Do you have tooling to help you fix that problem?:
#       * http://stackoverflow.com/questions/8626631/how-to-refactor-to-a-different-class-in-visual-studio
#       * http://stackoverflow.com/questions/9331352/eclipse-refactoring-a-java-method-into-a-another-class
#
#       So, maybe(?), kind of, but not really. Ouch.
#
# 9. I'll never refactor; I'll plan my code and write it perfectly the first time.
#       A: .... Are you kidding?
#
# 10. How do we organize code while maintaining the freedom to refactor (move
#       implementation around) without breaking any API's we've exposed?
#       A: Use free functions (or static classes if your language has no free
#       functions).
#
#       At worst, you'll need to update some `import` or `#include` statements
#       at the top of some files. IDE's tend to have refactor capabilities to help
#       you do this for free- or static functions around (because it's a simple
#       text transformation).
#
#       The cost of a refactor is much lower when you don't change argument lists.
#
# 11. Wait! Classes were a convenient way to group transformations. How am I
#       supposed to organize my code now?
#       A: Put logically grouped functionality in a single `namespace` or `file`
#       or  `package` or `module` or `static class`.
#
#       You're always free to organze your free functions *the exact same way*
#       you would have organized class methods. It's just much easier to re-
#       organize them as you learn more about the problem you're solving.
#
# 12. Encapsulation: We don't want callers to know what the rules structure looks like
#
# 13. Why? Because we want the freedom to change the structure without breaking callers
#       A: Make `rules` an opaque object.
#       A: There are once again two cases to consider here:
#           1. callers are using your recommended API:
def recommended_api_use():
    rules = build_rules_from_iterable(["a", "c", "a", "b"])
    result = apply_rules(rules, ["a", "c", "b", "x", "c", "a"])
#           2. callers are doing inadvisable modifications:
def not_recommended_api_use():
    rules = build_rules_from_iterable(["a", "c", "a", "b"])
    rules = inadvisable_modification(rules)
    result = apply_rules(rules, ["a", "c", "b", "x", "c", "a"])
#
#           If you change the structure of `rules` returned from
#           `build_rules_from_iterable`, and update `apply_rules` to match,
#           the code will run correctly without modification in case 1.
#
#           Case 1. is what you hope to achieve with OOP style.
#
#           Case 2. is what you hope to prevent with OOP style. Why did I write
#           the cases in functional style instead of OOP style? Because you can't
#           write case 2. in OOP style. You're trying to prevent it after all.
#           The question is, why prevent it?
#               1. Security?
#                   A: It's trivial to read bytes out of a structure in memory
#                       so you gain no security.
#               2. Avoiding spurious support requests?
#                   A: If use case 2 is common and your OOP API doesn't implement
#                       it, you'll probably get people requesting you add the
#                       feature. If you don't want to support the feature, you
#                       don't have to; your customers have already figured out
#                       how to work around it.
#               Your customer is not stupid; they have their own problems to solve
#               Support requests inform you of how your customers are using the code
#               The more flexibility your customers have for experimenting with
#               your API, the more they might teach you about the problem you're
#               solving.
