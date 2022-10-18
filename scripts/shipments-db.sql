create table if not exists orders
(
    id           bigint not null
        constraint orders_pk
            primary key,
    price        real,
    status       varchar(255),
    date_created varchar(255)
);


create table if not exists shipments
(
    id  bigint not null
        primary key,
    order_id     bigint not null
        constraint shipments_orders_id_fk
            references orders
            on update cascade on delete cascade,
    date_created varchar(255),
    status       varchar(25)
);

INSERT INTO public.orders (id, price, status, date_created) VALUES (1, 1000, 'Completed', '2022-10-19 00:15:00');
INSERT INTO public.orders (id, price, status, date_created) VALUES (2, 2000, 'Pending', '2022-10-19 00:16:00');
INSERT INTO public.orders (id, price, status, date_created) VALUES (3, 3000, 'Failed', '2022-10-19 00:17:00');
INSERT INTO public.shipments (id, order_id, date_created, status) VALUES (1, 1, '2022-10-19 00:20:00', 'Pending');
INSERT INTO public.shipments (id, order_id, date_created, status) VALUES (2, 2, '2022-10-19 00:20:00', 'Rejected');

