// a pony port of http://studygolang.com/resources/153
use "time"
use "random"

actor Main
  let numprocs: U64 = 8
  let env: Env
  let samples: U64 = 100_000_000
  var running: U64
  var results: F64 = 0

  new create(env': Env) =>
    env = env'
    running = numprocs
    var i: U64 = 0
    while i < numprocs do
      Worker(Time.nanos(), samples/numprocs, this)
      i = i+1
    end

  be result(res: F64) =>
    results = results + res
    running = running - 1
    if running == 0 then
      env.out.write((results/F64.from[U64](numprocs)).string() + "\n")
    end

actor Worker
  
  new create(seed: U64, samples:U64, main: Main) =>
    let rng = MT(seed)
    var done = samples
    var inside: U64 = 0
    /*let adjust = F64.max_value() / F64.max_value().sqrt()*/
    while done > 0 do
      let x = rng.real() //* adjust
      let y = rng.real() //* adjust
      if ((x*x) + (y*y)) <= 1 then
        inside = inside + 1
      end
      done = done - 1
    end
    var result = F64.from[U64](inside)/F64.from[U64](samples)
    result = result * 4
    main.result(result)
