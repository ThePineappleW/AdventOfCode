;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-advanced-reader.ss" "lang")((modname day2) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #t #t none #f () #f)))
;; LoSexpr --> Num
(define (calc-score lst op)
  (foldr (λ(round acc) (+ acc (op (first round) (second round)))) 0 (sep-pairs lst)))

;; LoStr --> LoLoStr
(define (sep-pairs lst)
  (zip (filter (λ(x) (member? x '(A B C))) lst) (filter (λ(x) (member? x '(X Y Z))) lst)))

;; LoX LoX --> LoLoX
(define (zip l1 l2) (map (λ(x1 x2) (list x1 x2)) l1 l2))

;; Sym Sym --> Bool
(define (win? them you)
  (or (and (symbol=? 'A them) (symbol=? 'Y you))
      (and (symbol=? 'B them) (symbol=? 'Z you))
      (and (symbol=? 'C them) (symbol=? 'X you))))

;; Sym Sym --> Bool
(define (draw? them you)
  (or (and (symbol=? 'A them) (symbol=? 'X you))
      (and (symbol=? 'B them) (symbol=? 'Y you))
      (and (symbol=? 'C them) (symbol=? 'Z you))))

;; Sym Sym --> Number
(define (get-score them you)
  (+ (score you)
     (cond [(win? them you) 6]
           [(draw? them you) 3]
           [else 0])))

;; Sym --> Num
(define (score throw)
  (cond [(symbol=? throw 'X) 1]
        [(symbol=? throw 'Y) 2]
        [(symbol=? throw 'Z) 3]))

;; Sym Sym --> Num
(define (get-score-outcome them you) (get-score them (get-yours them you)))

;; Sym Sym --> Sym
(define (get-yours theirs outcome)
  (cond [(and (symbol=? theirs 'A) (symbol=? outcome 'X)) 'Z]
        [(and (symbol=? theirs 'A) (symbol=? outcome 'Y)) 'X]
        [(and (symbol=? theirs 'A) (symbol=? outcome 'Z)) 'Y]
        [(and (symbol=? theirs 'B) (symbol=? outcome 'X)) 'X]
        [(and (symbol=? theirs 'B) (symbol=? outcome 'Y)) 'Y]
        [(and (symbol=? theirs 'B) (symbol=? outcome 'Z)) 'Z]
        [(and (symbol=? theirs 'C) (symbol=? outcome 'X)) 'Y]
        [(and (symbol=? theirs 'C) (symbol=? outcome 'Y)) 'Z]
        [(and (symbol=? theirs 'C) (symbol=? outcome 'Z)) 'X]))