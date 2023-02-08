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

struct NoisyDrop;

impl Drop for NoisyDrop {
    // drop 方法会在作用域结束后, 自动释放
    fn drop(&mut self) {
        println!("dropping!");
    }
}

fn main() {
    {
        #[warn(unused_variables)]
        let _nd = NoisyDrop;
        println!("before drop...");
        // `nd` goes out of scope and is dropped.
    }
    println!("after drop!");

    let a =1;
    let b = a;
    let c = a;
    println!("{c}");
    couter_func();
    // the `Mutex` lives here now
    let s: Mutex<State> = Default::default();
    for _ in 0..10 {
        // and we must lock it to call `foo`
        s.lock().foo();
    }
    lock_test();
    variable_test();
}

fn lock_test() {
    // 使用`Mutex`结构体的关联函数创建新的互斥锁实例
    let m = Mutex::new(5);

    {
        // 获取锁，然后deref为`m`的引用
        // lock返回的是Result
        let mut num = m.lock();
        *num = 6;
        // 锁自动被drop [逻辑一]
    }
    {
        // 本方法能正常执行完毕, 证明 逻辑一 生效
        let mut num = m.lock();
        *num += 1;
        // 测试锁是否会被自动释放
        // 下列注释打开, 将造成死锁
        // let mut num = m.lock();
        // *num += 1;
    }
    println!("m = {:?}", m);
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

fn variable_test() {
    let mut x = 42;

    let a = &mut x;
    println!("a = {a}");

    let b = &mut x;
    println!("b = {b}");
}
