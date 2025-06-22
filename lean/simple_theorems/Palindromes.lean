-- This file is an exercise based on the Palindromes example from lean-lang.org.
-- Your task is to fill in the `sorry` placeholders with the correct definitions and proofs.

-- An inductive predicate to specify whether a list is a palindrome.
inductive Palindrome : List α → Prop where
  | nil      : Palindrome []
  | single   : (a : α) → Palindrome [a]
  | sandwich : (a : α) → Palindrome as → Palindrome ([a] ++ as ++ [a])

-- Prove that the reverse of a palindrome is a palindrome.
theorem palindrome_reverse (h : Palindrome as) : Palindrome as.reverse := by
  sorry

-- Prove that if a list is a palindrome, its reverse is equal to itself.
theorem reverse_eq_of_palindrome (h : Palindrome as) : as.reverse = as := by
  sorry

-- Prove palindrome_reverse again, this time using reverse_eq_of_palindrome.
example (h : Palindrome as) : Palindrome as.reverse := by
  sorry

-- Define a function that returns the last element of a non-empty list.
def List.last : (as : List α) → as ≠ [] → α :=
  sorry

-- Prove that for a non-empty list, dropping the last element and appending it back yields the original list.
@[simp] theorem List.dropLast_append_last (h : as ≠ []) : as.dropLast ++ [as.last h] = as := by
  sorry

-- Define an auxiliary induction principle for lists that mirrors the structure of the Palindrome predicate.
theorem List.palindrome_ind (motive : List α → Prop)
    (h₁ : motive [])
    (h₂ : (a : α) → motive [a])
    (h₃ : (a b : α) → (as : List α) → motive as → motive ([a] ++ as ++ [b]))
    (as : List α)
    : motive as :=
  sorry

-- Use the new induction principle to prove that if a list's reverse equals itself, it is a palindrome.
theorem List.palindrome_of_eq_reverse (h : as.reverse = as) : Palindrome as := by
  induction as using palindrome_ind
  sorry

-- Define a function that checks if a list is a palindrome.
-- This requires that the elements of the list have decidable equality.
def List.isPalindrome [DecidableEq α] (as : List α) : Bool :=
  sorry

-- Prove that the isPalindrome function is correct.
theorem List.isPalindrome_correct [DecidableEq α] (as : List α) : as.isPalindrome ↔ Palindrome as := by
  sorry

-- Once the definitions and proofs above are complete, these examples should work.
-- You can uncomment them to test your work.

-- #eval [1, 2, 1].isPalindrome
-- #eval [1, 2, 3, 1].isPalindrome

-- example : [1, 2, 1].isPalindrome := rfl
-- example : [1, 2, 2, 1].isPalindrome := rfl
-- example : ![1, 2, 3, 1].isPalindrome := rfl
