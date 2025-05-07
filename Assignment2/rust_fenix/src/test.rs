#[allow(dead_code)]
fn print(input: u64) -> () {
    for i in 0..7 {
        for j in 0..8 {
            print!("{}", (input >> (j + i*8)) & 1);
        }
        print!("\n");
    }
    print!("\n");
}

fn to_u64(input: [[u8; 8]; 7]) -> u64 {
    let mut res = 0;
    for i in 0..7 {
        for j in 0..8 {
            if input[i][j] > 0 {
                res ^= 1 << (j + i*8);
            }
        }
    }

    return res;
}

#[allow(non_snake_case)]
fn test() {
    let current_player = [
        [1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ];
    let other_player = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 1, 1],
    ];

    let pos: [usize; 2] = [2, 0];

    let current_player = to_u64(current_player);
    let other_player = to_u64(other_player);
    
    let takes: fn (u64, [usize; 2]) -> u64 = |board, pos| {
        let mut mask = 0;
        let index = pos[0] + pos[1] * 8;
        if pos[0] > 1 {
            if board & (1 << (index-1)) != 0 {
                mask ^= 1 << (index-2);
            }
        }
        if pos[1] > 1 {
            if board & (1 << (index-8)) != 0 {
                mask ^= 1 << (index-16);
            }
        }
        if pos[0] < 6 {
            if board & (1 << (index+1)) != 0 {
                mask ^= 1 << (index+2);
            }
        }
        if pos[1] < 6 {
            if board & (1 << (index+8)) != 0 {
                mask ^= 1 << (index+16);
            }
        }
        return mask;
    };
    let no_takes: fn (u64, [usize; 2]) -> u64 = |board, pos| {
        let mut mask = 0;
        let index = pos[0] + pos[1] * 8;
        if pos[0] > 0 {
            if board & (1 << (index-1)) == 0 {
                mask ^= 1 << (index-1);
            }
        }
        if pos[1] > 0 {
            if board & (1 << (index-8)) == 0 {
                mask ^= 1 << (index-8);
            }
        }
        if pos[0] < 7 {
            if board & (1 << (index+1)) == 0 {
                mask ^= 1 << (index+1);
            }
        }
        if pos[1] < 7 {
            if board & (1 << (index+8)) == 0 {
                mask ^= 1 << (index+8);
            }
        }
        return mask;
    };
    // print(no_takes(current_player|other_player, pos));
    print(no_takes(current_player|other_player, pos));

    // let vertical_line: u64 = 0x1010101010101;
    // print(vertical_line << (pos_index) ); // ok
    // print(vertical_line.reverse_bits() >> (63-(4 + 6*8) + 8)); // ok
    // print((vertical_line << (pos_index)) & /* uniquement membre de droite car bottom a déjà été traité */ (vertical_line.reverse_bits() >> (63+8-(4 + 6*8))));
}