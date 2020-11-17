replaceChar = '-';

// Clean a string with the replaceChar to just a space
// Can be used to display clean text form the database
function cleanString(input) {
    while (input.indexOf(replaceChar) != -1) {
        input = input.replace(replaceChar, ' ');
    }
    return input;
}