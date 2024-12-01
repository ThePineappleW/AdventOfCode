import Day4
import Data.Text (replace, pack, unpack)

-- 1. Split input on blocks.
-- 2 For each block:
--      1. split on lines
--      2. Build an Int -> Int function:
--          1. Function contains list of ranges
--          2. If input in a range, 

-- (Dest, Src, Length)
type Mapping = (Int, Int, Int)

officialSeeds = [4188359137, 37519573, 3736161691, 172346126, 2590035450, 66446591, 209124047, 106578880, 1404892542, 30069991, 3014689843, 117426545, 2169439765, 226325492, 1511958436, 177344330, 1822605035, 51025110, 382778843, 823998526]
seedRanges = [[4188359137..(4188359137 + 37519573)], [3736161691..13736161691 + 72346126], [2590035450..2590035450 + 66446591], [209124047..209124047 + 106578880], [1404892542..1404892542 + 30069991], [3014689843..3014689843 + 117426545], [2169439765..2169439765 + 226325492], [1511958436..1511958436 + 177344330], [1822605035..1822605035 + 51025110], [382778843..382778843 + 823998526]]

transform :: Mapping -> Int -> (Int -> Int) -> Int
transform mapping n successor =
    if inRange n mapping
        then mappedVal n mapping
        else successor n
    
inRange :: Int -> Mapping -> Bool
inRange n (_, src, len) = 
    -- elem n [src..(src + (len - 1))]
    (src <= n) && (n < src + len)

-- assumes that `n` is in `mapping`; i.e. ignores length.
mappedVal :: Int -> Mapping -> Int
mappedVal n (dest, src, _) = 
    (n - src) + dest
    
getMapping :: [Mapping] -> Int -> Int
getMapping []     n = n
getMapping (m:ms) n = transform m n (getMapping ms)

findLowestLocation :: [Int] -> [[Mapping]] -> Int
findLowestLocation seeds mappings= 
    let mapFuncs = map getMapping mappings
        location = (\seed -> foldl (\x y -> y x) seed mapFuncs)
        locations = map location seeds
    in minimum locations

parseInput :: String -> IO()
parseInput filepath =
    do
        input <- readFile filepath
        let input' = replaceNewline input
            blocks = split '$' input'
            seeds:blocks' = map (split '\n') blocks
            headlessBlocks = map tail blocks'
            mappings = map (map lineToMapping) headlessBlocks
            result = findLowestLocation officialSeeds mappings
            
            result' = (map (\r -> minimum (map findLowestLocation r)) seedRanges)
            in print result
            
lineToMapping :: String -> Mapping
lineToMapping line =
     thruplify (map string2int (split ' ' line))
     
replaceNewline :: String -> String
replaceNewline = unpack . replace (pack "\n\n") (pack "$") . pack

thruplify :: [Int] -> (Int, Int, Int)
thruplify lst =
    if length lst == 3
        then let (x:y:z:_) = lst in (x, y, z)
        else (0, 0, 0)


