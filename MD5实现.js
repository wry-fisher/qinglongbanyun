function md5(inputString) {
    function leftRotate(x, n) {
        return (x << n) | (x >>> (32 - n));
    }

    function addUnsigned(a, b) {
        const lower = (a & 0xFFFF) + (b & 0xFFFF);
        const upper = (a >>> 16) + (b >>> 16) + (lower >>> 16);
        return (lower & 0xFFFF) + (upper & 0xFFFF) << 16;
    }

    const padding = [0x80, ...Array(Math.ceil((inputString.length + 8) / 64) * 64 - inputString.length - 9)];
    const lengthHi = (inputString.length * 8) >>> 31;
    const lengthLo = inputString.length * 8 & 0xFFFFFFFF;
    padding.push(lengthLo, lengthHi);

    const state = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476];
    const chunks = [];

    for (let i = 0; i < padding.length; i += 64) {
        const chunk = padding.slice(i, i + 64);
        chunks.push(chunk);
    }
    
    const s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21];
    const r = [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
            1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12,
            5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2,
            0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9
        ];

    for (const chunk of chunks) {
        let a = state[0], b = state[1], c = state[2], d = state[3];

        for (let i = 0; i < 64; i++) {
            const f = i < 16 ? (b & c) | (~b & d)
                : i < 32 ? (d & b) | (~d & c)
                : i < 48 ? b ^ c ^ d
                : c ^ (b | ~d);

            const k = i < 16 ? 0x5A827999
                : i < 32 ? 0x6ED9EBA1
                : i < 48 ? 0x8F1BBCDC
                : 0xCA62C1D6;

            const temp = addUnsigned(addUnsigned(a, f), addUnsigned(addUnsigned(leftRotate(b, s[i]), k), chunk[r[i]]));

            a = d;
            d = c;
            c = leftRotate(b, 30);
            b = temp;
        }

    return state.map(n => n.toString(16).padStart(8, '0')).join('');
        }

}    
    module.exports = { md5 };
console.log(md5("action=qiandao&appkey=1f70a57fdf4061a7&auth=7adac21a4c74543141bf8e35e4877616&username=c0749b03aec5e331&eBRaFLkuJ5"))