use parking_lot::Mutex;

#[derive(Default)]
struct State {
    // no longer in a `Mutex`
    value: u64,
}

impl State {
    // now taking `&mut`
    fn foo(&mut self) {
        self.value += 4;
        self.bar();
        println!("exiting foo, value = {}", self.value);
    }

    fn bar(&mut self) {
        if self.value > 10 {
            self.value = 0
        }
    }
}

fn main() {
    couter_func();
    // the `Mutex` lives here now
    let s: Mutex<State> = Default::default();
    for _ in 0..10 {
        // and we must lock it to call `foo`
        s.lock().foo();
    }
}

fn couter_func() {
    let counter = Mutex::new(0_u64);

    crossbeam::scope(|s| {
        for _ in 0..3 {
            s.spawn(|_| {
                // let's increment it a "couple" times
                for _ in 0..100_000 {
                    *counter.lock() += 1;
                }
            });
        }
    })
    .unwrap();

    let counter = counter.into_inner();
    println!("final count: {counter}");
}
