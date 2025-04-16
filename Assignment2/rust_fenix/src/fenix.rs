use std::{fmt::{write, Display}, hash::{DefaultHasher, Hash, Hasher}};

const DIM_X: usize = 8;
const DIM_Y: usize = 7;

#[derive(PartialEq, Clone)]
pub enum Player {
    RedPlayer,
    BlackPlayer,
}
#[derive(PartialEq, Clone)]
pub enum PieceType {
    Soldat,
    General,
    King,
}
#[derive(PartialEq, Clone)]
pub struct Piece {
    player: Player,
    piece: PieceType,
}
#[derive(Hash, Clone)]
pub struct PlayerBoard {
    pub soldat_board: u64,
    pub general_board: u64,
    pub king_board: u64,
}
#[derive(PartialEq, PartialOrd)]
pub struct Action {
    start: [usize; 2],
    end: [usize; 2],
    removed: Vec<[usize; 2]>,
}
#[derive(Clone)]
pub struct FenixState {
    pub turn: usize,
    pub current_player: Player,
    pub red_player: PlayerBoard,
    pub black_player: PlayerBoard,
    pub is_terminal: bool,
    pub boring_turn: usize,
    pub history_boring_turn_hash: Vec<u64>,
    pub can_create_general: bool,
    pub can_create_king: bool,
}

#[allow(dead_code)]
impl FenixState {
    pub fn new() -> FenixState {
        let red_board = 0x0103070F1F3F;
        let black_board = 0xFCF8F0E0C08000;
        return FenixState {
            turn: 0,
            current_player: Player::RedPlayer,
            red_player: PlayerBoard{soldat_board: red_board, general_board: 0, king_board: 0 },
            black_player: PlayerBoard{soldat_board: black_board, general_board: 0, king_board: 0 },
            is_terminal: false,
            boring_turn: 0,
            history_boring_turn_hash: vec![],
            can_create_general: false,
            can_create_king: false,
        };
    }

    pub fn is_valid(&self) -> bool {
        let to_test = [self.black_player.soldat_board, self.black_player.general_board, self.black_player.king_board,
                                self.red_player.soldat_board, self.red_player.general_board, self.red_player.king_board];
        
        for i in 0..5 {
            for j in i+1..6 {
                if to_test[i] & to_test[j] != 0 {
                    return false;
                }
            }
        }

        return true;
    }

    pub fn utility(&self, player: Player) -> Option<Player> /* still need to make a choice on how to return who wins, new enum ? */ {
        if player == Player::RedPlayer {

        } else {

        }

        todo!();
    }

    pub fn get_piece(&self, x: usize, y:usize) -> Option<Piece> {
        if x >= DIM_X || y >= DIM_Y { return None }
        let index = x + y * DIM_X;

        let player;
        let piece;
        if ((self.red_player.soldat_board | self.red_player.general_board | self.red_player.king_board) >> index) & 1 == 1 {
            player = Player::RedPlayer;
            if (self.red_player.soldat_board >> index) & 1 == 1 {
                piece = PieceType::Soldat;
            }
            else if (self.red_player.general_board >> index) & 1 == 1 {
                piece = PieceType::General;
            }
            else {
                piece = PieceType::King;
            }
        }
        else if ((self.black_player.soldat_board | self.black_player.general_board | self.black_player.king_board) >> index) & 1 == 1 {
            player = Player::BlackPlayer;
            if (self.black_player.soldat_board >> index) & 1 == 1 {
                piece = PieceType::Soldat;
            }
            else if (self.black_player.general_board >> index) & 1 == 1 {
                piece = PieceType::General;
            }
            else {
                piece = PieceType::King;
            }
        }
        else {
            return None;
        }

        return Some(Piece{player, piece});
    }

    fn set_piece(&mut self, x: usize, y: usize, piece: Piece) -> () {
        self.red_player.soldat_board  &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;
        self.red_player.general_board &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;
        self.red_player.king_board    &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;

        self.black_player.soldat_board  &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;
        self.black_player.general_board &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;
        self.black_player.king_board    &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;

        match piece.player {
            Player::RedPlayer => {
                match piece.piece {
                    PieceType::Soldat  => self.red_player.soldat_board  |= 1 << (x + y * DIM_X),
                    PieceType::General => self.red_player.general_board |= 1 << (x + y * DIM_X),
                    PieceType::King    => self.red_player.king_board    |= 1 << (x + y * DIM_X),
                }
            },
            Player::BlackPlayer => {
                match piece.piece {
                    PieceType::Soldat =>   self.black_player.soldat_board |= 1 << (x + y * DIM_X),
                    PieceType::General => self.black_player.general_board |= 1 << (x + y * DIM_X),
                    PieceType::King =>       self.black_player.king_board |= 1 << (x + y * DIM_X),
                }
            },
        }
    }

    fn del_piece(&mut self, x: usize, y:usize) -> () {
        self.red_player.soldat_board  &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;
        self.red_player.general_board &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;
        self.red_player.king_board    &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;

        self.black_player.soldat_board  &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;
        self.black_player.general_board &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;
        self.black_player.king_board    &= (1 << 7*6) - (1 << (x + y * DIM_X)) - 1;
    }

    pub fn actions(&self) -> Vec<Action> {
        if self.turn < 10 {
            return self.setup_turn();
        }
        return self.max_actions();
    }

    pub fn result(&self, action: &Action) -> FenixState {
        let mut state = self.clone();

        let start_option = state.get_piece(action.start[0], action.start[1]);
        let end_option = state.get_piece(action.end[0], action.end[1]);

        if let Some(start_piece) = start_option {
            if start_piece.player != self.current_player { panic!("trying to move a piece of the other team from the current player\n"); }
            if let Some(end_piece) = end_option {
                if start_piece.player != end_piece.player { panic!("action from moving a piece onto another one which is a piece of the other team\n"); }
                else if end_piece.piece == PieceType::Soldat {
                    if state.can_create_general || state.turn < 10 {
                        state.del_piece(action.start[0], action.start[1]);
                        state.set_piece(action.end[0], action.end[1], Piece{player: start_piece.player, piece: PieceType::General });
                    }
                    panic!("action leads to creating a general while the player is not authorised to\n");
                }
                else if end_piece.piece == PieceType::General {
                    if state.can_create_king || state.turn < 10 {
                        state.del_piece(action.start[0], action.start[1]);
                        state.set_piece(action.end[0], action.end[1], Piece{player: start_piece.player, piece: PieceType::King });
                    }
                    panic!("action leads to creating a king while the player is not authorised to\n");
                }
                panic!("action leads to moving onto the king which is not a legal move\n");
            }
            else {
                state.del_piece(action.start[0], action.start[1]);
                state.set_piece(action.end[0], action.end[1], start_piece);
            }
        }
        else {
            panic!("action has no starting piece to move\n");
        }

        state.can_create_general = false;
        state.can_create_king = false;
        for pos in &action.removed {
            let removed_option = state.get_piece(pos[0], pos[1]);
            if let Some(removed_piece) = removed_option {
                if removed_piece.player != state.current_player {
                    if removed_piece.piece == PieceType::General { state.can_create_general = true; }
                    else if removed_piece.piece == PieceType::King { state.can_create_king = true; }
                    state.del_piece(pos[0], pos[1]);
                }
                panic!("action removes a piece of the team of the current player\n");
            }
            else { panic!("action removes a piece that does not exist\n"); }
        }

        state.turn += 1;
        state.current_player = match state.current_player {
            Player::RedPlayer => Player::BlackPlayer,
            Player::BlackPlayer => Player::RedPlayer,
        };

        if action.removed.len() > 0 {
            state.boring_turn = 0;
            state.history_boring_turn_hash = vec![];
        }
        else if state.turn > 10 {
            state.boring_turn += 1;

            let mut s = DefaultHasher::new();
            state.hash(&mut s);
            let hash = s.finish();
            state.history_boring_turn_hash.push(hash);

            let mut count = 0;
            for hashed in &state.history_boring_turn_hash {
                if *hashed == hash { 
                    count += 1;
                    if count == 3 {
                        state.is_terminal = true;
                        break;
                    }
                }
            }
        }
        
        if state.boring_turn >= 50 {
            state.is_terminal = true;
        } if state.turn <= 10 && state.actions().len() == 0 {
            state.is_terminal = true;
        } 
        if state.turn > 10 {
            match state.current_player {
                Player::RedPlayer => {
                    if state.black_player.king_board == 0 {
                        state.is_terminal = true;
                    }
                },
                Player::BlackPlayer => {
                    if state.red_player.king_board == 0 {
                        state.is_terminal = true;
                    }
                },
            }
        }
        if state.black_player.soldat_board | state.black_player.general_board | state.black_player.king_board == 0
            || state.red_player.soldat_board | state.red_player.general_board | state.red_player.king_board == 0 {
            state.is_terminal = true;
        }

        return state;
    }

    fn has_piece(&self, player: Player) -> bool {
        match player {
            Player::RedPlayer => return self.red_player.soldat_board | self.red_player.general_board | self.red_player.king_board != 0,
            Player::BlackPlayer => return self.black_player.soldat_board | self.black_player.general_board | self.black_player.king_board != 0,
        }
    }

    fn max_actions(&self) -> Vec<Action> {
        let mut actions = vec![];
        let mut max_token_removed = 0;

        let current_player_board;
        let other_player_board;
        if self.current_player == Player::RedPlayer {
            current_player_board = self.red_player.soldat_board | self.red_player.general_board | self.red_player.king_board;
            other_player_board = self.black_player.soldat_board | self.black_player.general_board | self.black_player.king_board;
        } else {
            current_player_board = self.black_player.soldat_board | self.black_player.general_board | self.black_player.king_board;
            other_player_board = self.red_player.soldat_board | self.red_player.general_board | self.red_player.king_board;
        }

        for x in 0..DIM_X {
            for y in 0..DIM_Y {
                if let Some(piece) = self.get_piece(x, y) {
                    if piece.player == self.current_player {
                        let piece_actions = match piece.piece {
                            PieceType::Soldat => self.get_soldat_actions([x,y], current_player_board, other_player_board),
                            PieceType::General => self.get_general_actions([x,y], current_player_board, other_player_board),
                            PieceType::King => self.get_king_actions([x,y], current_player_board, other_player_board),
                        };
                        for piece_action in piece_actions {
                            let mut count_tokens = 0;
                            for pos in &piece_action.removed {
                                if let Some(piece) = self.get_piece(pos[0], pos[1]) {
                                    match piece.piece {
                                        PieceType::Soldat => count_tokens += 1,
                                        PieceType::General => count_tokens += 2,
                                        PieceType::King => count_tokens += 3,
                                    }
                                }
                            }
                            if count_tokens > max_token_removed {
                                max_token_removed = count_tokens;
                                actions.clear();
                                actions.push(piece_action);
                            } else if count_tokens == max_token_removed {
                                actions.push(piece_action);
                            }
                        }
                    }
                }
            }
        }

        actions.iter().fold(vec![], |mut acc, item| {
            let mut temp = item.removed.clone();
            temp.sort();
            let new_item = Action{start: item.start, end: item.end, removed: temp};
            
            if !acc.contains(&new_item) {
                acc.push(new_item);
            }
            
            return acc;
        });

        return actions;
    }

    fn get_soldat_actions(&self, pos: [usize; 2], current_player_board: u64, other_player_board: u64) -> Vec<Action> {
        let takes: fn (u64, [usize; 2]) -> u64 = |board, pos| {
            let mut mask = 0;
            let index = pos[0] + pos[1] * DIM_X;
            if pos[0] > 1 {
                if board & (1 << (index-1)) != 0 {
                    mask ^= 1 << (index-2);
                }
            }
            if pos[1] > 1 {
                if board & (1 << (index-DIM_X)) != 0 {
                    mask ^= 1 << (index-2*DIM_X);
                }
            }
            if pos[0] < 6 {
                if board & (1 << (index+1)) != 0 {
                    mask ^= 1 << (index+2);
                }
            }
            if pos[1] < 6 {
                if board & (1 << (index+DIM_X)) != 0 {
                    mask ^= 1 << (index+2*DIM_X);
                }
            }
            return mask;
        };
        let no_takes: fn (u64, [usize; 2]) -> u64 = |board, pos| {
            let mut mask = 0;
            let index = pos[0] + pos[1] * DIM_X;
            if pos[0] > 0 {
                if board & (1 << (index-1)) == 0 {
                    mask ^= 1 << (index-1);
                }
            }
            if pos[1] > 0 {
                if board & (1 << (index-DIM_X)) == 0 {
                    mask ^= 1 << (index-DIM_X);
                }
            }
            if pos[0] < 7 {
                if board & (1 << (index+1)) == 0 {
                    mask ^= 1 << (index+1);
                }
            }
            if pos[1] < 7 {
                if board & (1 << (index+DIM_X)) == 0 {
                    mask ^= 1 << (index+DIM_X);
                }
            }
            return mask;
        };

        struct TempState {
            pos: [usize; 2],
            current_player_board: u64,
            other_player_board: u64,
            removed: Vec<[usize; 2]>,
        }

        let mut actions = vec![];
        let mut queue: Vec<TempState> = vec![];

        let mut new_takes = takes(other_player_board, pos) & !(current_player_board|other_player_board);
        if new_takes != 0 {
            while new_takes != 0 {
                let index = new_takes.ilog2();
                let new_removed = vec![[(index & 0b111) as usize, (index >> 3) as usize]];

                queue.push(
                    TempState {
                        pos: [(index & 0b111) as usize, (index >> 3) as usize],
                        current_player_board: current_player_board,
                        other_player_board: other_player_board ^ (1 << index),
                        removed: new_removed
                    }
                );

                new_takes ^= 1 << index;
            }
        } else {
            let mut new_moves = no_takes(current_player_board|other_player_board, pos);

            while new_moves != 0 {
                let index = new_moves.ilog2();
                actions.push(
                    Action {
                        start: pos,
                        end: [(index & 0b111) as usize, (index >> 3) as usize],
                        removed: vec![],
                    }
                );

                new_moves ^= 1 << index;
            }
        }
        if self.can_create_general { todo!(); }
        if self.can_create_king { todo!(); }
        
        while let Some(state) = queue.pop() {
            let mut new_takes = takes(state.other_player_board, state.pos) & !(state.current_player_board|state.other_player_board);
            if new_takes != 0 {
                while new_takes != 0 {
                    let index = new_takes.ilog2();
                    
                    let mut new_removed = state.removed.clone();
                    new_removed.push([(index & 0b111) as usize, (index >> 3) as usize]);

                    queue.push(
                        TempState {
                            pos: [(index & 0b111) as usize, (index >> 3) as usize],
                            current_player_board: state.current_player_board,
                            other_player_board: state.other_player_board ^ (1 << index),
                            removed: new_removed
                        }
                    );

                    new_takes ^= 1 << index;
                }
            } else {
                actions.push(Action { start: pos, end: state.pos, removed: state.removed });
            }
        }
        return actions
    }

    fn get_general_actions(&self, pos: [usize; 2], current_player_board: u64, other_player_board: u64) -> Vec<Action> {
        
        let no_takes: fn (u64, [usize; 2]) -> u64 = |board, pos| {
            let vertical_line: u64 = 0x1010101010101;
            let horizontal_line: u64 = 0xFF;

            let pos_index = (pos[0] + pos[1] * DIM_X) as u32;
            let mut mask = (vertical_line << pos[0]) ^ (horizontal_line << pos[1] * DIM_X);

            while mask & board != 0 {
                let index = (mask & board).ilog2();
                if index > pos_index {
                    if pos_index & 0b111 == index & 0b111 {
                        mask &= !(vertical_line << index);
                    } else {
                        mask &= !((horizontal_line >> (index & 0b111)) << index);
                    }
                } else {
                    if pos_index & 0b111 == index & 0b111 {
                        mask &= !(vertical_line.reverse_bits() >> (63 - index));
                    } else {
                        mask &= !((horizontal_line.reverse_bits() << (index & 0b111)) >> (63 - index));
                    }
                }
            }

            return mask;
        };

        let takes: fn (u64, [usize; 2]) -> u64 = |board, pos| {
            let vertical_line: u64 = 0x1010101010101;
            let horizontal_line: u64 = 0xFF;

            let pos_index = (pos[0] + pos[1] * 8) as u32;
            let mut mask = 0;

            if (vertical_line.wrapping_shl(pos_index + 8)) & board != 0 {
                mask |= vertical_line << (pos_index + 8);
            }
            if ((horizontal_line >> ((pos_index+1)&0b111)).wrapping_shl(pos_index + 1)) & board != 0 {
                mask |= (horizontal_line >> ((pos_index+1)&0b111)) << (pos_index + 1);
            }
            if (vertical_line.reverse_bits().wrapping_shr(63 - pos_index + 8)) & board != 0 {
                mask |= vertical_line.reverse_bits().wrapping_shr(63 - pos_index + 8);
            }
            if ((horizontal_line >> (7-((pos_index-1)&0b111))).reverse_bits().wrapping_shr(63 - pos_index + 1)) & board != 0 {
                mask |= (horizontal_line >> (7-((pos_index-1)&0b111))).reverse_bits().wrapping_shr(63 - pos_index + 1);
            }

            let mut masked_board = mask & board;
            while masked_board != 0 {
                let index = masked_board.ilog2();
                if index > pos_index {
                    if pos_index & 0b111 == index & 0b111 {
                        let l = (vertical_line << pos_index) & (vertical_line.reverse_bits() >> (63+8 - index));
                        if l & masked_board != 0 {
                            mask &= !(vertical_line << index);
                        } else {
                            mask &= !(l << 8);
                        }
                    } else {
                        let l = (horizontal_line << pos_index) & (horizontal_line.reverse_bits() >> (63+1 - index));
                        if l & masked_board != 0 {
                            mask &= !((horizontal_line >> (index&0b111)) << index);
                        } else {
                            mask &= !(l << 1);
                        }
                    }
                } else {
                    if pos_index & 0b111 == index & 0b111 {
                        let l = (vertical_line << index + 8) & (vertical_line.reverse_bits() >> (63 -pos_index));
                        if l & masked_board != 0 {
                            mask &= !(vertical_line.reverse_bits() >> (63 - index));
                        } else {
                            mask &= !(l >> 8);
                        }
                    } else {
                        let l = (horizontal_line << index + 1) & (horizontal_line.reverse_bits() >> (63 -pos_index));
                        if l & masked_board != 0 {
                            mask &= !((horizontal_line.reverse_bits() << (7-(index&0b111))) >> (63 - index));
                        } else {
                            mask &= !(l >> 1);
                        }
                    }
                }
                masked_board = mask & board;
            }

            return mask;
        };

        struct TempState {
            pos: [usize; 2],
            current_player_board: u64,
            other_player_board: u64,
            removed: Vec<[usize; 2]>,
        }

        let mut actions = vec![];
        let mut queue: Vec<TempState> = vec![];

        let mut new_takes = takes(other_player_board, pos) & no_takes(current_player_board, pos);
        if new_takes != 0 {
            while new_takes != 0 {
                let index = new_takes.ilog2();
                let new_removed = vec![[(index&0b111) as usize, (index >> 3) as usize]];

                queue.push(
                    TempState {
                        pos: [(index&0b111) as usize, (index >> 3) as usize],
                        current_player_board: current_player_board,
                        other_player_board: other_player_board ^ (1 << index),
                        removed: new_removed
                    }
                );

                new_takes ^= 1 << index;
            }
        } else {
            let mut new_moves = no_takes(current_player_board, pos);
            while new_moves != 0 {
                let index = new_moves.ilog2();
                actions.push(
                    Action {
                        start: pos,
                        end: [(index&0b111) as usize, (index >> 3) as usize],
                        removed: vec![],
                    }
                );

                new_moves ^= 1 << index;
            }
        }

        while let Some(state) = queue.pop() {
            let mut new_takes = takes(state.other_player_board, state.pos) & no_takes(state.current_player_board, state.pos);
            if new_takes != 0 {
                while new_takes != 0 {
                    let index = new_takes.ilog2();

                    let mut new_removed = state.removed.clone();
                    new_removed.push([(index&0b111) as usize, (index >> 3) as usize]);

                    queue.push(
                        TempState {
                            pos: [(index&0b111) as usize, (index >> 3) as usize],
                            current_player_board: state.current_player_board,
                            other_player_board: state.other_player_board ^ (1 << index),
                            removed: new_removed
                        }
                    );

                    new_takes ^= 1 << index;
                }
            } else {
                actions.push(Action { start: pos, end: state.pos, removed: state.removed });
            }
        }
        
        return actions;
    }

    fn get_king_actions(&self, pos: [usize; 2], current_player_board: u64, other_player_board: u64) -> Vec<Action> {
        let takes: fn (u64, [usize; 2]) -> u64 = |board, pos| {
            let mut mask = 0;
            let index = pos[0] + pos[1] * DIM_X;
            if pos[0] > 1 {
                if board & (1 << (index-1)) != 0 {
                    mask ^= 1 << (index-2);
                }
                if pos[1] > 1 {
                    if board & (1 << (index-1+DIM_X)) != 0 {
                        mask ^= 1 << (index-2+2*DIM_X);
                    }
                }
                if pos[1] < 6 {
                    if board & (1 << (index-1-DIM_X)) != 0 {
                        mask ^= 1 << (index-2-2*DIM_X);
                    }
                }
            }
            if pos[1] > 1 {
                if board & (1 << (index-DIM_X)) != 0 {
                    mask ^= 1 << (index-2*DIM_X);
                }
            }
            if pos[0] < 6 {
                if board & (1 << (index+1)) != 0 {
                    mask ^= 1 << (index+2);
                }
                if pos[1] > 1 {
                    if board & (1 << (index+1-DIM_X)) != 0 {
                        mask ^= 1 << (index+2-2*DIM_X);
                    }
                }
                if pos[1] < 6 {
                    if board & (1 << (index+1+DIM_X)) != 0 {
                        mask ^= 1 << (index+2+2*DIM_X);
                    }
                }
            }
            if pos[1] < 6 {
                if board & (1 << (index+DIM_X)) != 0 {
                    mask ^= 1 << (index+2*DIM_X);
                }
            }
            return mask;
        };
        
        let no_takes: fn (u64, [usize; 2]) -> u64 = |board, pos| {
            let mut mask = 0;
            let index = pos[0] + pos[1] * DIM_X;
            if pos[0] > 0 {
                if board & (1 << (index-1)) != 0 {
                    mask ^= 1 << (index-1);
                }
                if pos[1] > 0 {
                    if board & (1 << (index-1-DIM_X)) != 0 {
                        mask ^= 1 << (index-1-DIM_X);
                    }
                }
                if pos[1] < 7 {
                    if board & (1 << (index-1+DIM_X)) != 0 {
                        mask ^= 1 << (index-1+DIM_X);
                    }
                }
            }
            if pos[1] > 0 {
                if board & (1 << (index-DIM_X)) != 0 {
                    mask ^= 1 << (index-DIM_X);
                }
            }
            if pos[0] < 7 {
                if board & (1 << (index+1)) != 0 {
                    mask ^= 1 << (index+1);
                }
                if pos[1] > 0 {
                    if board & (1 << (index+1-DIM_X)) != 0 {
                        mask ^= 1 << (index+1-DIM_X);
                    }
                }
                if pos[1] < 7 {
                    if board & (1 << (index+1+DIM_X)) != 0 {
                        mask ^= 1 << (index+1+DIM_X);
                    }
                }
            }
            if pos[1] < 7 {
                if board & (1 << (index+DIM_X)) != 0 {
                    mask ^= 1 << (index+DIM_X);
                }
            }
            return mask;
        };

        struct TempState {
            pos: [usize; 2],
            current_player_board: u64,
            other_player_board: u64,
            removed: Vec<[usize; 2]>,
        }

        let mut actions = vec![];
        let mut queue: Vec<TempState> = vec![];

        let mut new_takes = takes(other_player_board, pos) & !(current_player_board|other_player_board);
        if new_takes != 0 {
            while new_takes != 0 {
                let index = new_takes.ilog2();
                let new_removed = vec![[(index & 0b111) as usize, (index >> 3) as usize]];

                queue.push(
                    TempState {
                        pos: [(index & 0b111) as usize, (index >> 3) as usize],
                        current_player_board: current_player_board,
                        other_player_board: other_player_board ^ (1 << index),
                        removed: new_removed
                    }
                );

                new_takes ^= 1 << index;
            }
        } else {
            let mut new_moves = no_takes(current_player_board|other_player_board, pos);
            while new_moves != 0 {
                let index = new_moves.ilog2();
                actions.push(
                    Action {
                        start: pos,
                        end: [(index & 0b111) as usize, (index >> 3) as usize],
                        removed: vec![],
                    }
                );

                new_moves ^= 1 << index;
            }
        }
        
        while let Some(state) = queue.pop() {
            let mut new_takes = takes(state.other_player_board, state.pos) & !(current_player_board|other_player_board);
            if new_takes != 0 {
                while new_takes != 0 {
                    let index = new_takes.ilog2();
                    
                    let mut new_removed = state.removed.clone();
                    new_removed.push([(index & 0b111) as usize, (index >> 3) as usize]);

                    queue.push(
                        TempState {
                            pos: [(index & 0b111) as usize, (index >> 3) as usize],
                            current_player_board: state.current_player_board,
                            other_player_board: state.other_player_board ^ (1 << index),
                            removed: new_removed
                        }
                    );

                    new_takes ^= 1 << index;
                }
            } else {
                actions.push(Action { start: pos, end: state.pos, removed: state.removed });
            }
        }
        
        return actions
    }

    fn setup_turn(&self) -> Vec<Action> {
        let mut actions = Vec::new();
        let cond1;
        let cond2;
        match self.current_player {
            Player::RedPlayer => {
                cond1 = self.red_player.general_board.count_ones() < 4;
                cond2 = self.red_player.king_board != 0;
            },
            Player::BlackPlayer => {
                cond1 = self.black_player.general_board.count_ones() < 4;
                cond2 = self.black_player.king_board != 0;
            },
        }
        
        let get_pos = |x:usize, y:usize| {
            let mut res: Vec<[usize; 2]> = vec![];
            if x == 0 { res.push([1, y]); }
            else if x == DIM_X-1 { res.push([x-1, y]); }
            else { res.push([x-1, y]); res.push([x+1, y]); }
            
            if y == 0 { res.push([x, 1]); }
            else if y == DIM_X-1 { res.push([x, y-1]); }
            else { res.push([x, y-1]); res.push([x, y+1]); }

            return res;
        };
        
        for x in 0..DIM_X {
            for y in 0..DIM_Y {
                if let Some(piece) = self.get_piece(x, y) {
                    if self.current_player == piece.player && PieceType::Soldat == piece.piece {
                        for pos in get_pos(x,y) {
                            if let Some(other_piece) = self.get_piece(pos[0], pos[1]) {
                                if other_piece.player == self.current_player && 
                                        ((other_piece.piece == PieceType::Soldat && cond1) || (other_piece.piece == PieceType::General && cond2)) { 
                                    actions.push(Action { start: [x,y], end: pos, removed: vec![] });
                                }
                            }
                        }
                    }
                }
            }
        }
        return actions;
    }
}

impl Display for FenixState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut res = String::with_capacity((5*DIM_X + 2) * (2*DIM_Y + 1));

        let new_line = {
            let mut res = String::with_capacity(5*DIM_X + 2);
            for _ in 0..5*DIM_X+1 {
                res.push('-');
            }
            res.push('\n');
            res
        };

        res.push_str(&new_line);
        for y in 0..DIM_Y {
            res.push('|');
            for x in 0..DIM_X {
                res.push(' ');
                let option = self.get_piece(x, y);
                if let Some(piece) = option {
                    match piece.player {
                        Player::RedPlayer => res.push(' '),
                        Player::BlackPlayer => res.push('-'),
                    }
                    match piece.piece {
                        PieceType::Soldat => res.push('1'),
                        PieceType::General => res.push('2'),
                        PieceType::King => res.push('3'),
                    }
                }
                else {
                    res.push(' ');
                    res.push(' ');
                }

                res.push(' ');
                res.push('|');
            }
            res.push('\n');
            res.push_str(&new_line);
        }

        return write(f, format_args!("{}", res));
    }
}

impl Hash for FenixState {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.red_player.hash(state);
        self.black_player.hash(state);
    }
}

impl Display for Action {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut res = String::new();
        res.push_str(&format!("({},{}) -> ({},{}) : ", self.start[0], self.start[1], self.end[0], self.end[1]));

        for pos in &self.removed {
            res.push_str(&format!("({}, {}), ", pos[0], pos[1]));
        }
        res.pop();
        res.pop();

        return write(f, format_args!("{}", &res));
    }
}

#[allow(dead_code)]
pub fn print(input: u64) -> () {
    for y in 0..DIM_Y {
        for x in 0..DIM_X {
            print!("{}", (input >> (x + y*DIM_X)) & 1);
        }
        print!("\n");
    }
    print!("\n");
}

#[allow(dead_code)]
pub fn print_vec(input: Vec<u64>) -> () {
    if input.is_empty() { return; }

    for y in 0..DIM_Y {
        for item in &input {
            for x in 0..DIM_X {
                print!("{}", (item >> (x + y*DIM_X)) & 1);
            }
            print!(" ");
        }
        print!("\n");
    }
    print!("\n");
}
