mod fenix;
use fenix::FenixState;

fn main() {
    let fenix_state = FenixState::new();
    println!("{}", fenix_state.actions().len());
    for action in fenix_state.actions() {
        println!("{}", action);
    }

    println!("{}", fenix_state);
}
