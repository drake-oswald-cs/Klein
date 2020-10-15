*
* Prolog
*
0:        LDC 4,6(7)     ; Calculate Return Address
1:        ST 4,2(6)     ; Store Return Address on the Stack Frame
2:        LDC 5,3(0)     ; Set New Status
3:        ST 5,0(5)     ; Store Current Status
4:        LDA 6,10(5)     ; Set New Top Pointer
6:        LD 4,0(0)     ; Load Returned Value
7:        OUT 4,0,0      ; Print Returned Value
8:        HALT 0,0,0      ; End Program
*
* main
*
9:        ST 1,1(5)     ; Store Previous R1
10:        ST 2,2(5)     ; Store Previous R2
11:        ST 3,3(5)     ; Store Previous R3
12:        ST 4,4(5)     ; Store Previous R4
13:        ST 5,5(5)     ; Store Previous R5
14:        ST 6,6(5)     ; Store Previous R6
15:        LD 1,-2(5)     ; Load Arg 0 into reg 1
16:        LDC 2,0(0)     ; Loading Number 0 into register 2
17:        LDC 3,1(0)     ; Loading Number 1 into register 3
18:        ST 1,2(6)     ; Store Arg 1 at memLocation 2
19:        ST 2,3(6)     ; Store Arg 2 at memLocation 3
20:        ST 3,4(6)     ; Store Arg 3 at memLocation 4
21:        LDA 4,5(7)     ; Calculate Return Address
22:        ST 4,5(6)     ; Store Return Address on the Stack Frame
23:        ST 5,6(6)     ; Store Current Status
24:        LDA 5,6(6)     ; Set New Status
25:        LDA 6,34(5)     ; Set New Top Pointer
27:        LD 4,0(6)     ; Restoring tempVariable t3 into register 4
28:        LD 4,1(6)     ; Load Returned Value
29:        ST 4,-3(5)     ; Store Return Value
30:        LD 1,1(5)     ; Restoring Previous R1
31:        LD 2,2(5)     ; Restoring Previous R2
32:        LD 3,3(5)     ; Restoring Previous R3
33:        LD 4,4(5)     ; Restoring Previous R4
34:        LD 6,6(5)     ; Restoring Previous R6
35:        LD 5,5(5)     ; Restoring Previous R5
36:        LDA 6,-4(5)     ; Set Top Pointer Back
37:        LD 5,0(5)     ; Set Status Pointer Back
38:        LD 7,3(6)     ; Jump Back To Wherever Called From
*
* findGreatest
*
39:        ST 1,1(5)     ; Store Previous R1
40:        ST 2,2(5)     ; Store Previous R2
41:        ST 3,3(5)     ; Store Previous R3
42:        ST 4,4(5)     ; Store Previous R4
43:        ST 5,5(5)     ; Store Previous R5
44:        ST 6,6(5)     ; Store Previous R6
45:        LD 1,-3(5)     ; Load Arg 1 into reg 1
46:        LDC 2,9(0)     ; Loading Number 9 into register 2
47:        SUB 3,1,2      ; Subtracting reg 1 and reg 2
48:        JEQ 3,2(7)     ; Checking if boolean exprssion is true
49:        LDC 3,0(0)     ; Load False into reg 3
50:        LDA 7,1(7)     ; Jump over True
51:        LDC 3,1(0)     ; Load True into reg 3
52:        ST 3,-24(6)     ; Store Previous register 3 contents t7 in mem Location -24
56:        LD 3,-3(5)     ; Load Arg 1 into reg 3
57:        LD 4,-4(5)     ; Load Arg 0 into reg 4
58:        ST 3,2(6)     ; Store Arg 3 at memLocation 2
59:        ST 4,3(6)     ; Store Arg 4 at memLocation 3
60:        ST 4,-22(6)     ; Store Previous register 4 contents t9 in mem Location -22
61:        LDA 4,6(7)     ; Calculate Return Address
62:        ST 4,4(6)     ; Store Return Address on the Stack Frame
63:        LD 4,-22(6)     ; Restoring tempVariable t9 into register 4
64:        ST 5,5(6)     ; Store Current Status
65:        LDA 5,5(6)     ; Set New Status
66:        LDA 6,28(5)     ; Set New Top Pointer
68:        ST 1,-26(6)     ; Store Previous register 1 contents t5 in mem Location -26
69:        LD 1,-21(6)     ; Restoring tempVariable t10 into register 1
70:        LD 1,1(6)     ; Load Returned Value
71:        ST 3,-23(6)     ; Store Previous register 3 contents t8 in mem Location -23
72:        LD 3,-2(5)     ; Load Arg 2 into reg 3
73:        ST 1,-21(6)     ; Store Previous register 1 contents t10 in mem Location -21
74:        LD 1,-4(5)     ; Load Arg 0 into reg 1
75:        ST 3,2(6)     ; Store Arg 3 at memLocation 2
76:        ST 1,3(6)     ; Store Arg 1 at memLocation 3
77:        ST 4,-22(6)     ; Store Previous register 4 contents t9 in mem Location -22
78:        LDA 4,6(7)     ; Calculate Return Address
79:        ST 4,4(6)     ; Store Return Address on the Stack Frame
80:        LD 4,-22(6)     ; Restoring tempVariable t9 into register 4
81:        ST 5,5(6)     ; Store Current Status
82:        LDA 5,5(6)     ; Set New Status
83:        LDA 6,28(5)     ; Set New Top Pointer
85:        ST 3,-20(6)     ; Store Previous register 3 contents t11 in mem Location -20
86:        LD 3,-18(6)     ; Restoring tempVariable t13 into register 3
87:        LD 3,1(6)     ; Load Returned Value
88:        ST 1,-19(6)     ; Store Previous register 1 contents t12 in mem Location -19
89:        LD 1,-21(6)     ; Restoring tempVariable t10 into register 1
90:        ST 3,-18(6)     ; Store Previous register 3 contents t13 in mem Location -18
91:        SUB 3,1,3      ; Subtracting reg 1 and reg 3
92:        JLT 3,2(7)     ; Checking if boolean exprssion is true
93:        LDC 3,0(0)     ; Load False into reg 3
94:        LDA 7,1(7)     ; Jump over True
95:        LDC 3,1(0)     ; Load True into reg 3
96:        ST 3,-17(6)     ; Store Previous register 3 contents t14 in mem Location -17
100:        LD 3,-2(5)     ; Load Arg 2 into reg 3
101:        ST 3,-27(6)     ; Store Previous register 3 contents t4 in mem Location -27
103:        LDC 3,9(0)     ; Loading Number 9 into register 3
104:        ST 3,-27(6)     ; Store Previous register 3 contents t4 in mem Location -27
105:        LD 3,-27(6)     ; Loading t4 into reg 3
106:        ST 3,-27(6)     ; Store Previous register 3 contents t4 in mem Location -27
108:        LD 3,-3(5)     ; Load Arg 1 into reg 3
109:        ST 1,-21(6)     ; Store Previous register 1 contents t10 in mem Location -21
110:        LD 1,-4(5)     ; Load Arg 0 into reg 1
111:        ST 3,2(6)     ; Store Arg 3 at memLocation 2
112:        ST 1,3(6)     ; Store Arg 1 at memLocation 3
113:        ST 4,-22(6)     ; Store Previous register 4 contents t9 in mem Location -22
114:        LDA 4,6(7)     ; Calculate Return Address
115:        ST 4,4(6)     ; Store Return Address on the Stack Frame
116:        LD 4,-22(6)     ; Restoring tempVariable t9 into register 4
117:        ST 5,5(6)     ; Store Current Status
118:        LDA 5,5(6)     ; Set New Status
119:        LDA 6,28(5)     ; Set New Top Pointer
121:        ST 3,-16(6)     ; Store Previous register 3 contents t15 in mem Location -16
122:        LD 3,-14(6)     ; Restoring tempVariable t17 into register 3
123:        LD 3,1(6)     ; Load Returned Value
124:        ST 1,-15(6)     ; Store Previous register 1 contents t16 in mem Location -15
125:        LD 1,-2(5)     ; Load Arg 2 into reg 1
126:        ST 3,-14(6)     ; Store Previous register 3 contents t17 in mem Location -14
127:        LD 3,-4(5)     ; Load Arg 0 into reg 3
128:        ST 1,2(6)     ; Store Arg 1 at memLocation 2
129:        ST 3,3(6)     ; Store Arg 3 at memLocation 3
130:        ST 4,-22(6)     ; Store Previous register 4 contents t9 in mem Location -22
131:        LDA 4,6(7)     ; Calculate Return Address
132:        ST 4,4(6)     ; Store Return Address on the Stack Frame
133:        LD 4,-22(6)     ; Restoring tempVariable t9 into register 4
134:        ST 5,5(6)     ; Store Current Status
135:        LDA 5,5(6)     ; Set New Status
136:        LDA 6,28(5)     ; Set New Top Pointer
138:        ST 1,-13(6)     ; Store Previous register 1 contents t18 in mem Location -13
139:        LD 1,-11(6)     ; Restoring tempVariable t20 into register 1
140:        LD 1,1(6)     ; Load Returned Value
141:        ST 3,-12(6)     ; Store Previous register 3 contents t19 in mem Location -12
142:        LD 3,-14(6)     ; Restoring tempVariable t17 into register 3
143:        ST 1,-11(6)     ; Store Previous register 1 contents t20 in mem Location -11
144:        SUB 1,3,1      ; Subtracting reg 3 and reg 1
145:        JLT 1,2(7)     ; Checking if boolean exprssion is true
146:        LDC 1,0(0)     ; Load False into reg 1
147:        LDA 7,1(7)     ; Jump over True
148:        LDC 1,1(0)     ; Load True into reg 1
149:        ST 1,-10(6)     ; Store Previous register 1 contents t21 in mem Location -10
153:        LD 1,-4(5)     ; Load Arg 0 into reg 1
154:        ST 3,-14(6)     ; Store Previous register 3 contents t17 in mem Location -14
155:        LD 3,-3(5)     ; Load Arg 1 into reg 3
156:        ST 1,-9(6)     ; Store Previous register 1 contents t22 in mem Location -9
157:        LDC 1,1(0)     ; Loading Number 1 into register 1
158:        ST 3,-8(6)     ; Store Previous register 3 contents t23 in mem Location -8
159:        ADD 3,3,1      ; Compute Operation ADD on reg 3 and reg 1
160:        ST 1,-7(6)     ; Store Previous register 1 contents t24 in mem Location -7
161:        LD 1,-2(5)     ; Load Arg 2 into reg 1
162:        ST 3,-6(6)     ; Store Previous register 3 contents t25 in mem Location -6
163:        LD 3,-9(6)     ; Restoring tempVariable t22 into register 3
164:        ST 3,2(6)     ; Store Arg 3 at memLocation 2
165:        ST 1,-5(6)     ; Store Previous register 1 contents t26 in mem Location -5
166:        LD 1,-6(6)     ; Restoring tempVariable t25 into register 1
167:        ST 1,3(6)     ; Store Arg 1 at memLocation 3
168:        ST 3,-9(6)     ; Store Previous register 3 contents t22 in mem Location -9
169:        LD 3,-5(6)     ; Restoring tempVariable t26 into register 3
170:        ST 3,4(6)     ; Store Arg 3 at memLocation 4
171:        ST 4,-22(6)     ; Store Previous register 4 contents t9 in mem Location -22
172:        LDA 4,6(7)     ; Calculate Return Address
173:        ST 4,5(6)     ; Store Return Address on the Stack Frame
174:        LD 4,-22(6)     ; Restoring tempVariable t9 into register 4
175:        ST 5,6(6)     ; Store Current Status
176:        LDA 5,6(6)     ; Set New Status
177:        LDA 6,34(5)     ; Set New Top Pointer
179:        ST 1,-6(6)     ; Store Previous register 1 contents t25 in mem Location -6
180:        LD 1,-27(6)     ; Restoring tempVariable t4 into register 1
181:        LD 1,1(6)     ; Load Returned Value
182:        ST 1,-27(6)     ; Store Previous register 1 contents t4 in mem Location -27
184:        LD 1,-4(5)     ; Load Arg 0 into reg 1
185:        ST 3,-5(6)     ; Store Previous register 3 contents t26 in mem Location -5
186:        LD 3,-3(5)     ; Load Arg 1 into reg 3
187:        ST 1,-4(6)     ; Store Previous register 1 contents t27 in mem Location -4
188:        LDC 1,1(0)     ; Loading Number 1 into register 1
189:        ST 3,-3(6)     ; Store Previous register 3 contents t28 in mem Location -3
190:        ADD 3,3,1      ; Compute Operation ADD on reg 3 and reg 1
191:        ST 1,-2(6)     ; Store Previous register 1 contents t29 in mem Location -2
192:        LD 1,-3(5)     ; Load Arg 1 into reg 1
193:        ST 3,-1(6)     ; Store Previous register 3 contents t30 in mem Location -1
194:        LD 3,-4(6)     ; Restoring tempVariable t27 into register 3
195:        ST 3,2(6)     ; Store Arg 3 at memLocation 2
196:        ST 1,0(6)     ; Store Previous register 1 contents t31 in mem Location 0
197:        LD 1,-1(6)     ; Restoring tempVariable t30 into register 1
198:        ST 1,3(6)     ; Store Arg 1 at memLocation 3
199:        ST 3,-4(6)     ; Store Previous register 3 contents t27 in mem Location -4
200:        LD 3,0(6)     ; Restoring tempVariable t31 into register 3
201:        ST 3,4(6)     ; Store Arg 3 at memLocation 4
202:        ST 4,-22(6)     ; Store Previous register 4 contents t9 in mem Location -22
203:        LDA 4,6(7)     ; Calculate Return Address
204:        ST 4,5(6)     ; Store Return Address on the Stack Frame
205:        LD 4,-22(6)     ; Restoring tempVariable t9 into register 4
206:        ST 5,6(6)     ; Store Current Status
207:        LDA 5,6(6)     ; Set New Status
208:        LDA 6,34(5)     ; Set New Top Pointer
210:        ST 1,-1(6)     ; Store Previous register 1 contents t30 in mem Location -1
211:        LD 1,-27(6)     ; Restoring tempVariable t4 into register 1
212:        LD 1,1(6)     ; Load Returned Value
213:        ST 1,-27(6)     ; Store Previous register 1 contents t4 in mem Location -27
214:        LD 1,-27(6)     ; Loading t4 into reg 1
215:        ST 1,-27(6)     ; Store Previous register 1 contents t4 in mem Location -27
216:        LD 1,-27(6)     ; Loading t4 into reg 1
217:        ST 1,-5(5)     ; Store Return Value
218:        LD 1,1(5)     ; Restoring Previous R1
219:        LD 2,2(5)     ; Restoring Previous R2
220:        LD 3,3(5)     ; Restoring Previous R3
221:        LD 4,4(5)     ; Restoring Previous R4
222:        LD 6,6(5)     ; Restoring Previous R6
223:        LD 5,5(5)     ; Restoring Previous R5
224:        LDA 6,-6(5)     ; Set Top Pointer Back
225:        LD 5,0(5)     ; Set Status Pointer Back
226:        LD 7,5(6)     ; Jump Back To Wherever Called From
*
* count
*
227:        ST 1,1(5)     ; Store Previous R1
228:        ST 2,2(5)     ; Store Previous R2
229:        ST 3,3(5)     ; Store Previous R3
230:        ST 4,4(5)     ; Store Previous R4
231:        ST 5,5(5)     ; Store Previous R5
232:        ST 6,6(5)     ; Store Previous R6
233:        LD 1,-2(5)     ; Load Arg 1 into reg 1
234:        LDC 2,10(0)     ; Loading Number 10 into register 2
235:        SUB 3,1,2      ; Subtracting reg 1 and reg 2
236:        JLT 3,2(7)     ; Checking if boolean exprssion is true
237:        LDC 3,0(0)     ; Load False into reg 3
238:        LDA 7,1(7)     ; Jump over True
239:        LDC 3,1(0)     ; Load True into reg 3
240:        ST 3,-18(6)     ; Store Previous register 3 contents t35 in mem Location -18
244:        LD 3,-3(5)     ; Load Arg 0 into reg 3
245:        LD 4,-2(5)     ; Load Arg 1 into reg 4
246:        ST 3,-17(6)     ; Store Previous register 3 contents t36 in mem Location -17
247:        SUB 3,3,4      ; Subtracting reg 3 and reg 4
248:        JEQ 3,2(7)     ; Checking if boolean exprssion is true
249:        LDC 3,0(0)     ; Load False into reg 3
250:        LDA 7,1(7)     ; Jump over True
251:        LDC 3,1(0)     ; Load True into reg 3
252:        ST 3,-15(6)     ; Store Previous register 3 contents t38 in mem Location -15
256:        LDC 3,1(0)     ; Loading Number 1 into register 3
257:        ST 3,-21(6)     ; Store Previous register 3 contents t32 in mem Location -21
259:        LDC 3,0(0)     ; Loading Number 0 into register 3
260:        ST 3,-21(6)     ; Store Previous register 3 contents t32 in mem Location -21
261:        LD 3,-21(6)     ; Loading t32 into reg 3
262:        ST 3,-21(6)     ; Store Previous register 3 contents t32 in mem Location -21
264:        LD 3,-3(5)     ; Load Arg 0 into reg 3
265:        ST 1,-20(6)     ; Store Previous register 1 contents t33 in mem Location -20
266:        LD 1,-2(5)     ; Load Arg 1 into reg 1
267:        ST 3,-14(6)     ; Store Previous register 3 contents t39 in mem Location -14
268:        LDC 3,10(0)     ; Loading Number 10 into register 3
269:        ST 1,2(6)     ; Store Arg 1 at memLocation 2
270:        ST 3,3(6)     ; Store Arg 3 at memLocation 3
271:        ST 4,-16(6)     ; Store Previous register 4 contents t37 in mem Location -16
272:        LDA 4,6(7)     ; Calculate Return Address
273:        ST 4,4(6)     ; Store Return Address on the Stack Frame
274:        LD 4,-16(6)     ; Restoring tempVariable t37 into register 4
275:        ST 5,5(6)     ; Store Current Status
276:        LDA 5,5(6)     ; Set New Status
277:        LDA 6,13(5)     ; Set New Top Pointer
279:        ST 1,-13(6)     ; Store Previous register 1 contents t40 in mem Location -13
280:        LD 1,-11(6)     ; Restoring tempVariable t42 into register 1
281:        LD 1,1(6)     ; Load Returned Value
282:        ST 3,-12(6)     ; Store Previous register 3 contents t41 in mem Location -12
283:        LD 3,-14(6)     ; Restoring tempVariable t39 into register 3
284:        ST 1,-11(6)     ; Store Previous register 1 contents t42 in mem Location -11
285:        SUB 1,3,1      ; Subtracting reg 3 and reg 1
286:        JEQ 1,2(7)     ; Checking if boolean exprssion is true
287:        LDC 1,0(0)     ; Load False into reg 1
288:        LDA 7,1(7)     ; Jump over True
289:        LDC 1,1(0)     ; Load True into reg 1
290:        ST 1,-10(6)     ; Store Previous register 1 contents t43 in mem Location -10
294:        LDC 1,1(0)     ; Loading Number 1 into register 1
295:        ST 3,-14(6)     ; Store Previous register 3 contents t39 in mem Location -14
296:        LD 3,-3(5)     ; Load Arg 0 into reg 3
297:        ST 1,-9(6)     ; Store Previous register 1 contents t44 in mem Location -9
298:        LD 1,-2(5)     ; Load Arg 1 into reg 1
299:        ST 3,-8(6)     ; Store Previous register 3 contents t45 in mem Location -8
300:        LDC 3,10(0)     ; Loading Number 10 into register 3
301:        ST 1,-7(6)     ; Store Previous register 1 contents t46 in mem Location -7
302:        DIV 1,1,3      ; Compute Operation DIV on reg 1 and reg 3
303:        ST 3,-6(6)     ; Store Previous register 3 contents t47 in mem Location -6
304:        LD 3,-8(6)     ; Restoring tempVariable t45 into register 3
305:        ST 3,2(6)     ; Store Arg 3 at memLocation 2
306:        ST 1,3(6)     ; Store Arg 1 at memLocation 3
307:        ST 4,-16(6)     ; Store Previous register 4 contents t37 in mem Location -16
308:        LDA 4,6(7)     ; Calculate Return Address
309:        ST 4,4(6)     ; Store Return Address on the Stack Frame
310:        LD 4,-16(6)     ; Restoring tempVariable t37 into register 4
311:        ST 5,5(6)     ; Store Current Status
312:        LDA 5,5(6)     ; Set New Status
313:        LDA 6,28(5)     ; Set New Top Pointer
315:        ST 1,-5(6)     ; Store Previous register 1 contents t48 in mem Location -5
316:        LD 1,-4(6)     ; Restoring tempVariable t49 into register 1
317:        LD 1,1(6)     ; Load Returned Value
318:        ST 3,-8(6)     ; Store Previous register 3 contents t45 in mem Location -8
319:        LD 3,-9(6)     ; Restoring tempVariable t44 into register 3
320:        ST 1,-4(6)     ; Store Previous register 1 contents t49 in mem Location -4
321:        ADD 1,3,1      ; Compute Operation ADD on reg 3 and reg 1
322:        ST 1,-21(6)     ; Store Previous register 1 contents t32 in mem Location -21
324:        LD 1,-3(5)     ; Load Arg 0 into reg 1
325:        ST 3,-9(6)     ; Store Previous register 3 contents t44 in mem Location -9
326:        LD 3,-2(5)     ; Load Arg 1 into reg 3
327:        ST 1,-3(6)     ; Store Previous register 1 contents t50 in mem Location -3
328:        LDC 1,10(0)     ; Loading Number 10 into register 1
329:        ST 3,-2(6)     ; Store Previous register 3 contents t51 in mem Location -2
330:        DIV 3,3,1      ; Compute Operation DIV on reg 3 and reg 1
331:        ST 1,-1(6)     ; Store Previous register 1 contents t52 in mem Location -1
332:        LD 1,-3(6)     ; Restoring tempVariable t50 into register 1
333:        ST 1,2(6)     ; Store Arg 1 at memLocation 2
334:        ST 3,3(6)     ; Store Arg 3 at memLocation 3
335:        ST 4,-16(6)     ; Store Previous register 4 contents t37 in mem Location -16
336:        LDA 4,6(7)     ; Calculate Return Address
337:        ST 4,4(6)     ; Store Return Address on the Stack Frame
338:        LD 4,-16(6)     ; Restoring tempVariable t37 into register 4
339:        ST 5,5(6)     ; Store Current Status
340:        LDA 5,5(6)     ; Set New Status
341:        LDA 6,28(5)     ; Set New Top Pointer
343:        ST 3,0(6)     ; Store Previous register 3 contents t53 in mem Location 0
344:        LD 3,-21(6)     ; Restoring tempVariable t32 into register 3
345:        LD 3,1(6)     ; Load Returned Value
346:        ST 3,-21(6)     ; Store Previous register 3 contents t32 in mem Location -21
347:        LD 3,-21(6)     ; Loading t32 into reg 3
348:        ST 3,-21(6)     ; Store Previous register 3 contents t32 in mem Location -21
349:        LD 3,-21(6)     ; Loading t32 into reg 3
350:        ST 3,-4(5)     ; Store Return Value
351:        LD 1,1(5)     ; Restoring Previous R1
352:        LD 2,2(5)     ; Restoring Previous R2
353:        LD 3,3(5)     ; Restoring Previous R3
354:        LD 4,4(5)     ; Restoring Previous R4
355:        LD 6,6(5)     ; Restoring Previous R6
356:        LD 5,5(5)     ; Restoring Previous R5
357:        LDA 6,-5(5)     ; Set Top Pointer Back
358:        LD 5,0(5)     ; Set Status Pointer Back
359:        LD 7,4(6)     ; Jump Back To Wherever Called From
*
* MOD
*
360:        ST 1,1(5)     ; Store Previous R1
361:        ST 2,2(5)     ; Store Previous R2
362:        ST 3,3(5)     ; Store Previous R3
363:        ST 4,4(5)     ; Store Previous R4
364:        ST 5,5(5)     ; Store Previous R5
365:        ST 6,6(5)     ; Store Previous R6
366:        LD 1,-3(5)     ; Load Arg 0 into reg 1
367:        LD 2,-3(5)     ; Load Arg 0 into reg 2
368:        LD 3,-2(5)     ; Load Arg 1 into reg 3
369:        DIV 4,2,3      ; Compute Operation DIV on reg 2 and reg 3
370:        ST 1,-6(6)     ; Store Previous register 1 contents t54 in mem Location -6
371:        LD 1,-2(5)     ; Load Arg 1 into reg 1
372:        ST 3,-4(6)     ; Store Previous register 3 contents t56 in mem Location -4
373:        MUL 3,4,1      ; Compute Operation MUL on reg 4 and reg 1
374:        ST 1,-2(6)     ; Store Previous register 1 contents t58 in mem Location -2
375:        LD 1,-6(6)     ; Restoring tempVariable t54 into register 1
376:        ST 3,-1(6)     ; Store Previous register 3 contents t59 in mem Location -1
377:        SUB 3,1,3      ; Compute Operation SUB on reg 1 and reg 3
378:        ST 3,-4(5)     ; Store Return Value
379:        LD 1,1(5)     ; Restoring Previous R1
380:        LD 2,2(5)     ; Restoring Previous R2
381:        LD 3,3(5)     ; Restoring Previous R3
382:        LD 4,4(5)     ; Restoring Previous R4
383:        LD 6,6(5)     ; Restoring Previous R6
384:        LD 5,5(5)     ; Restoring Previous R5
385:        LDA 6,-5(5)     ; Set Top Pointer Back
386:        LD 5,0(5)     ; Set Status Pointer Back
387:        LD 7,4(6)     ; Jump Back To Wherever Called From
*
* Branches
*
5:        LDC 7,9(0)     ; Jumping to main
26:        LDC 7,39(0)     ; Jumping to findGreatest
67:        LDC 7,227(0)     ; Jumping to count
84:        LDC 7,227(0)     ; Jumping to count
120:        LDC 7,227(0)     ; Jumping to count
137:        LDC 7,227(0)     ; Jumping to count
178:        LDC 7,39(0)     ; Jumping to findGreatest
209:        LDC 7,39(0)     ; Jumping to findGreatest
278:        LDC 7,360(0)     ; Jumping to MOD
314:        LDC 7,227(0)     ; Jumping to count
342:        LDC 7,227(0)     ; Jumping to count
*
* If Conditions
*
53:        ST 1,-27(6)     ; Store Previous register 1 contents t4 in mem Location -27
54:        LD 1,-24(6)     ; Restoring tempVariable t7 into register 1
55:        JEQ 1,108(0)     ; Jumping to 108 if reg 1 is false
97:        ST 3,0(6)     ; Store Previous register 3 contents t31 in mem Location 0
98:        LD 3,-17(6)     ; Restoring tempVariable t14 into register 3
99:        JEQ 3,103(0)     ; Jumping to 103 if reg 3 is false
150:        ST 1,-24(6)     ; Store Previous register 1 contents t7 in mem Location -24
151:        LD 1,-10(6)     ; Restoring tempVariable t21 into register 1
152:        JEQ 1,184(0)     ; Jumping to 184 if reg 1 is false
241:        ST 3,-21(6)     ; Store Previous register 3 contents t32 in mem Location -21
242:        LD 3,-18(6)     ; Restoring tempVariable t35 into register 3
243:        JEQ 3,264(0)     ; Jumping to 264 if reg 3 is false
253:        ST 1,-3(6)     ; Store Previous register 1 contents t50 in mem Location -3
254:        LD 1,-15(6)     ; Restoring tempVariable t38 into register 1
255:        JEQ 1,259(0)     ; Jumping to 259 if reg 1 is false
291:        ST 3,-18(6)     ; Store Previous register 3 contents t35 in mem Location -18
292:        LD 3,-10(6)     ; Restoring tempVariable t43 into register 3
293:        JEQ 3,324(0)     ; Jumping to 324 if reg 3 is false
*
* GoTo
*
102:        LDC 7,105(0)     ; Go to L3
107:        LDC 7,216(0)     ; Go to L1
183:        LDC 7,214(0)     ; Go to L5
258:        LDC 7,261(0)     ; Go to L9
263:        LDC 7,349(0)     ; Go to L7
323:        LDC 7,347(0)     ; Go to L11
