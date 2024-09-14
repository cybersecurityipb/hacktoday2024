import System.IO
import System.Exit
import Data.Char
import Data.List (elemIndex)

str = ['A'..'Z']
origin  = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
m1      = ".@Q'PAV^/MO9Z|EX};<>SI5,F`%4G$+JY(=N31W#D\"0L2&]6!87:B?U{\\K~CH-*)[_RT"
m2      = "Z>.+I9P_HQ'GF?^S,&RA4;2!U3#:{/NW7~BXTY8V`=@(K\"]J-O}1$0C<5*[\\LE%M)6D|"
m3      = ">=ALZVJP601}WG8N]2<!\\I;B/*S#E_?M+~|&%R7${[`4'.DKYU(F)T:@CXQ-5^,3H\"9O"

withIndices :: [a] -> [(Int, a)]
withIndices xs = [(i, x) | (i, x) <- zip [0..] xs]

tuplesToString :: [(Int, Char)] -> String
tuplesToString = map snd

mapIndicesToString :: [Int] -> String -> String
mapIndicesToString indices str = map (\i -> str !! i) indices

encrypt :: [Int] -> [Int] -> [Int]
encrypt text key = zipWith (\x y -> (x + y) `mod` 26) text key

processText :: String -> [Int]
processText = map (\c -> ord (toUpper c) - 65) . filter isAlpha

rebuildMessage :: String -> String -> String
rebuildMessage [] _ = []
rebuildMessage (c:cs) (x:xs)
    | isAlpha c = x : rebuildMessage cs xs
    | otherwise = c : rebuildMessage cs (x:xs)
rebuildMessage cs [] = cs

bijectiveMapper :: [(Int, Char)] -> String
bijectiveMapper [] = []
bijectiveMapper ((i, c):xs) = case elemIndex c origin of
    Just index ->
        let mapping = case i `mod` 3 of
                0 -> m1
                1 -> m2
                2 -> m3
        in mapping !! (index `mod` length mapping) : bijectiveMapper xs
    Nothing -> error $ "Character " ++ [c] ++ " not found in origin string"

main :: IO ()
main = do
    let key = "HACKTODAY"
    putStr "Enter the text: "
    hFlush stdout
    text <- getLine
    let asciiText = processText text
    let asciiKey = map (\c -> ord (toUpper c) - 65) (take (length asciiText) (cycle (filter isAlpha key)))

    let msg = mapIndicesToString (encrypt asciiText asciiKey) str

    putStrLn $"Done!"
    putStrLn $"Result: " ++ bijectiveMapper (withIndices (rebuildMessage text msg))