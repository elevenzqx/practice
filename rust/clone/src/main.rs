#[derive(Clone, Copy)]
pub enum Protection {
    Secure(SecureVersion),
    Insecure,
}

#[derive(Clone, Copy, Debug)]
pub enum SecureVersion {
    V1,
    V2,
    V2_1,
}

fn process(prot: &Protection) {
    match prot {
        Protection::Secure(version) => {
            println!("Hacker-safe thanks to protocol {version:?}");
        }
        Protection::Insecure => {
            println!("Come on in");
        }
    }
}

fn main() {
    // clone();
    let prot = Protection::Secure(SecureVersion::V2_1);
    process(&prot);
    process(&prot);
}