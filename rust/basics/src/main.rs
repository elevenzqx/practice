fn is_good() -> bool {
    true
}

fn main() {
    let msg = if is_good() {
        "It is good job"
    } else {
        "It isn't good, yet"
    };
    println!("{msg}");

    println!(
        "{}",
        if is_good() {
            "It is good"
        } else {
            "It isn't good, yet"
        }
    ); // 这里需要分号, 否则会报错

    // Rust also has match, which is sort of like a more powerful switch:
    let msg = match is_good() {
        true => "It is good",
        false => "It isn't good, yet",
    };
    println!("{msg}")
}
