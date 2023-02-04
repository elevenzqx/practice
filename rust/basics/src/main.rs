use rand::Rng;

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
    println!("{msg}");

    rand_function();

    process(Protection::Secure(SecureVersion::V2_1))
}

// 需要查找 crate 仓库依赖 https://crates.io/crates/rand/versions 并添加到 Cargo 依赖文件中
// 支持多值匹配
fn rand_function() {
    let msg = match rand::thread_rng().gen_range(0..=10) {
        // match only 10
        10 => "Overwhelming victory",
        // match anything 5 or above
        5.. => "Victory",
        // match anything else (fallback case)
        _ => "Defeat",
    };

    println!("{msg}")
}

// 枚举类型的使用
pub enum Protection {
    Secure (SecureVersion),
    #[deprecated = "using secure mode everywhere is now strongly recommended"]
    Insecure,
}

#[derive(Debug)]
pub enum SecureVersion {
    V1,
    V2,
    V2_1,
}

fn process(prot: Protection) {
    match prot {
        Protection::Secure (version) => {
            println!("No hackers plz, v: {version:?}");
        }
        // We still need to handle this case
        #[allow(deprecated)]
        Protection::Insecure => {
            println!("Come on in");
        }
    }
}
