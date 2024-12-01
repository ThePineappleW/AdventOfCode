module Day4 where

import Data.List (intersect)

totalPoints :: String -> IO()
totalPoints filepath =
    do
        input <- readFile filepath
        let cards  = dropLast (split '\n' input)
            points = sum (map countPoints cards)
        print points

countMatches :: String -> Int
countMatches [] = 0
countMatches input =
    let line         = drop 10 input
        numbers      = split '|' line
        win : my : _ = map parseNumbers numbers
    in length (intersect win my)

countPoints :: String -> Int
countPoints input = 
    let common = countMatches input
    in if common == 0
        then 0
        else 2 ^ (common - 1)

parseNumbers :: String -> [Int]
parseNumbers str = 
    [string2int x | x <- split ' ' str, length x > 0]

string2int :: String -> Int
string2int x = read x :: Int

split :: Eq a => a -> [a] -> [[a]]
split _ []  = []
split p lst = 
    foldr (\cur splits -> if cur == p
                            then []:splits
                            else (cur:head splits) : tail splits)
            [[]] lst

dropLast :: Eq a => [a] -> [a]
dropLast = reverse . tail . reverse

type Item = (Int, Int)

initCounts :: [Int] -> [Item]
initCounts = map (\x -> (x, 1))

cloneCards :: Item -> [Item] -> [Item]
cloneCards _ [] = []
cloneCards (0, _) xs = xs
cloneCards (depth, times) xs = 
    let (x, count) : rest = xs
    in (x, count + times) : cloneCards (depth - 1, times) rest

compute :: [Item] -> [Item]
compute [] = []
compute (x:xs) = x : (compute (cloneCards x xs))

countCards :: String -> IO()
countCards filepath =
    do
        input <- readFile filepath
        let cards  = dropLast (split '\n' input)
            items = initCounts (map countMatches cards)
            counts = map snd (compute items)
        print (sum counts)