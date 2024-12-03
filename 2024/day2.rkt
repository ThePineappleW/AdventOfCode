#lang racket

(require "utils/utils.rkt")
(require racket/set)
(require test-engine/racket-tests)


;; [List Number] -> [List Number]
;; Computes the changes between consecutive list items.
;; For a given list of length `n`, will return a list of length `n-1`,
;; unless `n` = 0 in which case an empty list is returned.
(define (diff lst)
  (if (or (null? lst) (null? (cdr lst)))
      '()
      (cons (- (second lst) (first lst))
            (diff (rest lst)))))

;; [List Integer] -> Boolean
;; Is this report safe?
;; A report is safe if it is empty, or
;; for every change in level `c`,
;; |c| is within [1,3] and all changes have the same sign.
(define (safe? report)
  (let ([d (list->set (diff report))])
    (or (set-empty? (set-subtract d (set 1 2 3)))
        (set-empty? (set-subtract d (set -1 -2 -3))))))

;; [List X] -> [List X]
;; Returns a list of lists, each missing one of the items.
;; Definitely the brute force solution.
(define (remove-each lst)
  (define (remove-nth lst n)
    (append (take lst n) (drop lst (+ 1 n))))
  (build-list (length lst) (λ(n) (remove-nth lst n))))

;; [List Integer] Boolean -> Boolean
;; If `dampen` is truthy, remove every level and see if any reports are safe.
;; Otherwise, check if the entire report is safe.
(define (safe-dampened report dampen)
  (or (safe? report)
      (and dampen
          (ormap safe? (remove-each report)))))

;; [List [List Int]] Int -> Int
;; Consumes the list of reports and
;; the (inclusive) threshold for unsafe levels.
(define (safe-reports reports dampen)
  (length (filter (λ(r) (safe-dampened r dampen)) reports)))

;; ([List Int] -> Int) Int Port -> Int
(define (solve-problem proc dampen port)
  (proc (read-rows port string->number " ") dampen))


;; Tests

(define given-test
  "7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9")

; Part 1

(check-expect (solve-problem safe-reports #f
                             (open-input-string given-test))
              2)

; Part 2

(check-expect (solve-problem safe-reports #t
                             (open-input-string given-test))
              4)

(test)