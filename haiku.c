// Compile:
// gcc haiku.c -o haiku
// Play:
// ./haiku | aplay -f cd
// // // //

main(){
    int i, s, d;
    int thirty = 44100 * 2 * 2 * 30;
    for(i = 0; i < thirty; i++) {
        d = i % (thirty / 100) + 1;
        s = i % d;
        putchar(s); 
    }
}
